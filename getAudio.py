import os
import pytubefix as pytube
import whisper
from moviepy import AudioFileClip
from transformers import pipeline

def baixar_audio(url, output_path='downloads'):
    yt = pytube.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    file_path = audio_stream.download(output_path)
    new_file_path = os.path.join(output_path, "audio.mp3")
    os.rename(file_path, new_file_path)
    return new_file_path

def converter_para_wav(audio_path):
    output_path = f'downloads/audio.wav'
    audio = AudioFileClip(audio_path)
    audio.write_audiofile(output_path, codec='pcm_s16le')
    os.remove(audio_path)
    return output_path

def transcrever_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    os.remove(audio_path)
    return result['text']

def resumir_texto(texto):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(texto)
    return summary[0]['summary_text']

def main():
    url = input("Digite a URL do vídeo do YouTube: ")
    print("Baixando áudio...")
    audio_mp3 = baixar_audio(url)
    
    print("Convertendo para WAV...")
    audio_wav = converter_para_wav(audio_mp3)
    
    print("Transcrevendo áudio...")
    texto = transcrever_audio(audio_wav)
    
    print("Resumindo texto...")
    texto = resumir_texto(texto)

    print("Resumo completo:")
    print(texto)

if __name__ == "__main__":
    main()
