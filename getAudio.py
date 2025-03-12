import os
import pytubefix as pytube
import whisper
from moviepy import AudioFileClip
from transformers import pipeline

def getAudio(url, output_path='downloads'):
    yt = pytube.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    file_path = audio_stream.download(output_path)
    new_file_path = os.path.join(output_path, "audio.mp3")
    os.rename(file_path, new_file_path)
    return new_file_path

def wavConverter(audio_path):
    output_path = f'downloads/audio.wav'
    audio = AudioFileClip(audio_path)
    audio.write_audiofile(output_path, codec='pcm_s16le')
    os.remove(audio_path)
    return output_path

def transcribeAudio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    return result['text']

def resumeText(texto):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(texto)
    return summary[0]['summary_text']

def main():
    url = input("Digite a URL do vídeo do YouTube: ")
    print("Baixando áudio...")
    audio_mp3 = getAudio(url)
    
    print("Convertendo para WAV...")
    audio_wav = wavConverter(audio_mp3)
    
    print("Transcrevendo áudio...")
    texto = transcribeAudio(audio_wav)
    
    print("Resumindo texto...")
    texto = resumeText(texto)

    print("Resumo completo:")
    print(texto)

if __name__ == "__main__":
    main()
