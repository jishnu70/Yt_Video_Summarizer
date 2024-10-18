from django.shortcuts import render
from django.http import JsonResponse
import os
from pytube import YouTube
from pydub import AudioSegment
from transformers import BartForConditionalGeneration, BartTokenizer
import whisper
import aiofiles
from asgiref.sync import sync_to_async
import asyncio
import json
import yt_dlp
# Create your views here.

# initalize the whisper model
whisper_model = whisper.load_model("base")
tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")

async def download_youtube_audio(url):
    output_path = os.path.join(os.getcwd(), 'temp_audio.wav')

    # Remove any existing file before downloading
    if os.path.exists(output_path):
        os.remove(output_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(os.getcwd(), 'temp_audio'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    try:
        print(f"Attempting to download from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"WAV file downloaded at: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading audio: {e}")
        raise

async def transcibe_the_audio(wav_file_path):
    if not os.path.exists(wav_file_path):
        raise FileNotFoundError(f"{wav_file_path} does not exist.")
    result = await sync_to_async(whisper_model.transcribe)(wav_file_path)
    return result["text"]

async def summerize_the_text(transcript):
    chunk_size = 1024
    summary_list = []
    
    # Split the transcript into chunks that fit within the token limit
    for i in range(0, len(transcript), chunk_size):
        chunk = transcript[i:i + chunk_size]
        inputs = tokenizer.encode(chunk, return_tensors="pt", max_length=chunk_size, truncation=True)
        summary_ids = model.generate(inputs, max_length=400, min_length=150, length_penalty=1.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summary_list.append(summary)
    
    # Combine all chunk summaries into one final summary
    final_summary = " ".join(summary_list)
    return final_summary

async def youtube_summary(request):
    if request.method == "POST":
        body = request.body
        data = json.loads(body)
        youtube_url = data.get("youtube_url")
        print(f"Received URL: {youtube_url}")

        if youtube_url:
            try:
                YouTube(youtube_url)    # to check if it is a valid url

                wav_file_path = await download_youtube_audio(youtube_url)
                print(f"WAV file downloaded at: {wav_file_path}")

                transcript = await transcibe_the_audio(wav_file_path)
                summary = await summerize_the_text(transcript)

                # clean up the text
                await sync_to_async(os.remove)(wav_file_path)

                return JsonResponse({"Summary":summary})
            except Exception as e:
                if "regex_search" in str(e):
                    return JsonResponse({'error': 'Enter a valid URL.'}, status=400)
                print(f"Error processing video: {e}")
                return JsonResponse({'error': 'There was an error processing the video.'}, status=500)
    return  JsonResponse({"error":"Invalid Request"}, status=400)

def index(request):
    return render(request, 'youtube_summary/index.html')