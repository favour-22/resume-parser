import spacy
import fitz
import re
import docx
import json

nlp = spacy.load("en_core_web_sm")

class ResumeParser:
    def __init__(self, file):
        self.file = file

    def parse_resume(self):
    # Check if the uploaded file is a PDF or Word file
        if self.file and self.file.filename.split(".")[-1].lower() in ["pdf", "docx"]:
            if self.file.filename.split(".")[-1].lower() == "pdf":
            # Open the PDF file in binary mode
                with fitz.open(stream=self.file.read(), filetype="pdf") as pdf_file:
                # Extracting the text from each page of the PDF file
                    text = ""
                for page in pdf_file:
                    text += page.get_text()
        elif self.file.filename.split(".")[-1].lower() == "docx":
            # Open the Word file and extract the text
            doc = docx.Document(self.file)
            text = "\n".join([para.text for para in doc.paragraphs])

        # Cleaning up the text
        text = " ".join(text.split())

        # Using Spacy to parse the text and extract relevant information
        doc = nlp(text)
        data = {}

        # Extracting honors and awards if available
        honors_and_awards = []
        honors_re = re.compile(r"\b\d{4}\b(.+)")
        matches = honors_re.findall(text)
        for match in matches:
            honors_and_awards.append(match.strip())
        data["honors_and_awards"] = honors_and_awards if honors_and_awards else None

        # Extracting the name of the individual
        name = ""
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text
                break
        data["name"] = name if name else None

        # Extracting age
        age = ""
        age_re = re.compile(r"\b\d{1,2}\b\s*(years old|yo|Y\.O\.|yrs|years)")
        match = age_re.search(text)
        if match:
            age = match.group(0)
        data["age"] = age if age else None

        # Extracting contact information
        contact = {}
        email_re = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
        phone_re = re.compile(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b")
        address_re = re.compile(r"\b\d+\s+([A-Za-z]+\s+){1,3}(St\.|Ave\.|Rd\.|Blvd\.|Ln\.)\b")
        linkedin_re = re.compile(r"linkedin.com/in/([A-Za-z0-9-]+)")
        github_re = re.compile(r"github.com/([A-Za-z0-9-]+)")
        website_re = re.compile(r"(?i)\b((?:https?:\/\/|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}\/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+([^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
        twitter_re = re.compile(r"twitter.com/([A-Za-z0-9_]+)")
        stackoverflow_re = re.compile(r"stackoverflow.com/users/(\d+)/")

        for token in doc:
            if token.like_email:
                match = email_re.search(token.text)
                if match:
                    contact["email"] = match.group(0)
            elif phone_re.search(token.text):
                match = phone_re.search(token.text)
                if match:
                    contact["phone"] = match.group(0)
            elif token.is_stop and token.nbor().is_title:
                match = address_re.search(f"{token.text} {token.nbor().text}")
                if match:
                    contact["address"] = match.group(0)
            elif linkedin_re.search(token.text):
                match = linkedin_re.search(token.text)
                if match:
                    contact["linkedin"] = match.group(1)
            elif github_re.search(token.text):
                match = github_re.search(token.text)
                if match:
                    contact["github"] = match.group(1)
            elif website_re.search(token.text):
                match = website_re.search(token.text)
                if match:
                    contact["website"] = match.group(0)
            elif twitter_re.search(token.text):
                match = twitter_re.search(token.text)
                if match:
                    contact["twitter"] = match.group(1)
            elif stackoverflow_re.search(token.text):
                match = stackoverflow_re.search(token.text)
                if match:
                    contact["stackoverflow"] = match.group(1)
        data["contact"] = contact if contact else None

        # Extracting education information
        education = []
        for ent in doc.ents:
            if ent.label_ == "ORG":
                education.append(ent.text)
        data["education"] = education if education else None

        # Extracting work experience
        work_experience = []
        work_re = re.compile(r"\b([A-Z][a-z]+\s+[0-9]{4})\s*-\s*([A-Z][a-z]+\s+[0-9]{4}|Present)\s*(.+)\s*")
        matches = work_re.findall(text)
        for match in matches:
            work_experience.append({
                "start_date": match[0],
                "end_date": match[1] if match[1] != "Present" else None,
                "position": match[2].split("at")[0].strip(),
                "company": match[2].split("at")[1].strip()
            })
        data["work_experience"] = work_experience if work_experience else None

        # Extracting skills
        skills = []
        for ent in doc.ents:
            if ent.label_ == "SKILL":
                skills.append(ent.text)
        data["skills"] = skills if skills else None

        # Return data as a JSON object
        return json.dumps(data)
        
        


    
    

