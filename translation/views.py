from django.shortcuts import render, redirect
from django.http import FileResponse
from django.contrib.auth import logout 
from .forms import LoginForm, RegistrationForm, UploadFileForm
from .models import RegistrationModel
from translation.service import readImage
from translation.utils import extract_text_from_pdf, read_image, summarize_parallel
import googletrans
import os
import re
import uuid
from gtts import gTTS
from googletrans import Translator
from django.http import HttpResponse

# Define PROJECT_PATH
# Move PROJECT_PATH one level up
PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 🔹 User Registration
def registration(request):
    status = False

    if request.method == "POST":
        registrationForm = RegistrationForm(request.POST)
        if registrationForm.is_valid():
            regModel = RegistrationModel()
            regModel.name = registrationForm.cleaned_data["name"]
            regModel.mobile = registrationForm.cleaned_data["mobile"]
            regModel.username = registrationForm.cleaned_data["username"]
            regModel.password = registrationForm.cleaned_data["password"]

            user = RegistrationModel.objects.filter(username=regModel.username).first()
            if user is None:
                try:
                    regModel.save()
                    status = True
                except Exception as e:
                    print("Error saving registration:", e)
                    status = False
            else:
                status = False

    if status:
        return render(request, 'index.html', {"message": "Registration successful!"})
    else:
        return render(request, 'registration.html', {"message": "User already exists"})



# 🔹 User Login
def user_login(request):
    if request.method == "POST":
        loginForm = LoginForm(request.POST)
        
        if loginForm.is_valid():
            uname = loginForm.cleaned_data["username"]
            upass = loginForm.cleaned_data["password"]
            user = RegistrationModel.objects.filter(username=uname, password=upass).first()
            print(user)
            if user:
                request.session["username"] = uname
                return redirect("translate_page")  # Redirect to translation page

            return render(request, "login.html", {"message": "Invalid username or Password"})

    return render(request, "login.html")  # Render login page for GET requests


# 🔹 User Logout
def logout_view(request):
    logout(request)
    return redirect('user_login')

# 🔹 Function to Process Video File
def process_video(video_path):
    """
    Extracts audio from video, converts it to text, summarizes the text.
    """
    try:
        # Extract Audio
        audio_path = video_path.replace(".mp4", ".wav")
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)

        # Convert Audio to Text
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            extracted_text = recognizer.recognize_google(audio_data)

        # Summarize Text
        summarized_text = summarize_parallel(extracted_text)
        
        # Clean Text
        clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', summarized_text)

        return clean_text  # Return final summarized text

    except Exception as e:
        print(f"Error processing video: {e}")
        return None

# 🔹 File Upload Handler
def handle_uploaded_file(f):
    upload_path = os.path.join(PROJECT_PATH, 'upload', f.name)
    with open(upload_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return upload_path  # Return file path for processing




def translate(input_text, input_lang, output_lang):
    """Translates text from input_lang to output_lang using googletrans."""
    if not input_text.strip():
        return "No text provided for translation."

    translator = Translator()
    
    try:
        translated_text = translator.translate(input_text, src=input_lang, dest=output_lang).text
        return translated_text
    except Exception as e:
        print(f"⚠️ Translation Error: {e}")
        return f"Translation failed: {str(e)}"

def translate_page(request):
    # Get the list of available languages
    languages = googletrans.LANGUAGES  # ✅ Make sure this is available

    return render(request, 'translate.html', {"languages": languages})

# 🔹 Prediction (Processing Function)
def predict(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            uploaded_file = request.FILES['file']
            input_lang = request.POST['input_lang']
            output_lang = request.POST['output_lang']
            file_path = handle_uploaded_file(uploaded_file)
            file_extension = uploaded_file.name.split(".")[-1].lower()
            
            # 🔹 Process File Based on Type
            if file_extension == "pdf":
                input_text = extract_text_from_pdf(file_path)
            elif file_extension in ["jpg", "jpeg", "png"]:
                input_text = readImage(file_path)
            elif file_extension in ["mp4", "avi", "mov", "mkv"]:
                input_text = process_video(file_path)  # Process Video Input
            else:
                return render(request, 'translate.html', {"message": "Unsupported file format"})
            
            # 🔹 Summarization
            summary_text = summarize_parallel(input_text)
            clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', summary_text)

            # 🔹 Translation
            output_text = translate(clean_text, input_lang, output_lang)

            # 🔹 Save Summary to a File
            doc_filename = f"{uuid.uuid4()}.txt"
            doc_filepath = os.path.join(PROJECT_PATH, 'documents', doc_filename)
            with open(doc_filepath, "w", encoding="utf-8") as f:
                f.write(str(output_text))

            # 🔹 Generate Audio Output
            audio_filename = f"{uuid.uuid4()}.mp3"
            audio_filepath = os.path.join(PROJECT_PATH, "static/audio", audio_filename)
            try:
                tts = gTTS(text=str(output_text), lang=output_lang, slow=False)
                tts.save(audio_filepath)
            except Exception as e:
                print("Error in Audio Generation:", e)
                audio_filename = None  # No audio if error occurs

            return render(request, 'translate.html', {
                "language": googletrans.LANGUAGES,
                "input": clean_text,
                "output": output_text,
                "doc_filename": doc_filename,
                "audio_filename": audio_filename
            })

        else:
            return render(request, 'translate.html', {"message": "Invalid form submission"})

# 🔹 File Download Function
def download(request):
    doc_filename = request.GET.get('file')
    doc_filepath = os.path.join(PROJECT_PATH, 'documents', doc_filename)

    if os.path.exists(doc_filepath):
        return FileResponse(open(doc_filepath, 'rb'), as_attachment=True)
    else:
        return render(request, 'translate.html', {"message": "File not found"})


#### Youtube  video trinscriber..
def yttranscriber(request):
    # Redirect to the Streamlit app running at localhost:8501
    return redirect("http://localhost:8501/")


# def yttranscriber(request):
#     # Ensure a valid response is returned
#     return HttpResponse("This is the yttranscriber view.")

