import whisper
from whisper.utils import get_writer

model = whisper.load_model("base")  # choose appropriate model
result = model.transcribe("തുടങ്ങിയ YouTube Channel എല്ലാം പൂട്ടി കെട്ടി! [RRa7WhEcP2A].mp4", language="ml", task="translate")  # or .wav, .mp4

writer = get_writer("srt", output_dir="./subs")
writer(result, "my_subtitles")  # saves 'my_subtitles.en.srt'
