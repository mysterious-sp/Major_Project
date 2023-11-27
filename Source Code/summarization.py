from transformers import pipeline
import requests
import json




# cfg
API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/knkarthick/MEETING_SUMMARY"
headers = {"Authorization": f"Bearer {API_KEY}"}
num_points = 5
min_length = 10
max_length = 50
audio_file_path = "AudioFile/audio.wav"
output_dir = "Output"



#utils
def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

def transcript_post_process(transcript,num_points):
  final_output = {}
  point = 0
  total_n = len(transcript['chunks'])
  divisions = int(total_n/num_points) + 1

  for iter,item in enumerate(transcript['chunks']):
    if iter%divisions == 0:
      point +=1
      final_output[f'text_{point}'] = ''
      final_output[f'timestep_{point}_start'] = transcript['chunks'][iter]['timestamp'][0]

    final_output[f'text_{point}'] += transcript['chunks'][iter]['text']

  return final_output

def summary_generation():
  end_time_step = transcript['chunks'][-1]['timestamp'][1]
  summary = {}
  for i in range(1,num_points+1):
    sum_output = query({
    "inputs": final_transcript[f'text_{i}'],
    "parameters": {"min_length":min_length,"max_length":max_length},
    "options": {"wait_for_model":True,},
  })
    summary[f'point_{i}'] = {}
    summary[f'point_{i}']['summary'] = sum_output[0]['summary_text']
    summary[f'point_{i}']['start_time_step'] = final_transcript[f'timestep_{i}_start']
    try:
      summary[f'point_{i}']['end_time_step'] = final_transcript[f'timestep_{i+1}_start']
    except:
      summary[f'point_{i}']['end_time_step'] = end_time_step

  json_object = json.dumps(summary)
  with open(f"{output_dir}/summary.json", "w") as outfile:
    outfile.write(json_object)

speech_pipeline = pipeline("automatic-speech-recognition",
                model="openai/whisper-tiny.en",
                chunk_length_s=30,
                return_timestamps=True,)


if __name__ == '__main__':
# run
  transcript = speech_pipeline(audio_file_path)
  print(transcript['text'])

  final_transcript= transcript_post_process(transcript,num_points)

  summary_generation()
