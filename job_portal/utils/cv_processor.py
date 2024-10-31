import PyPDF2
import anthropic
import os

class CVProcessor:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv('CLAUDE_API_KEY')
        )

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text

    def evaluate_cv(self, cv_text, job):
        prompt = f"""You are an HR expert evaluating job applications. Your task is to evaluate the provided CV against the job requirements and provide a structured response.

Please evaluate the CV using exactly the following format in your response:
Score: [Insert score 1-3]
Explanation: [Insert your detailed evaluation]

Scoring criteria:
1: Does not meet most of the job requirements
2: Meets some job requirements but lacks in key areas
3: Meets or exceeds all the job requirements and is an ideal fit

Job Details:
Title: {job.title}
Description: {job.description}
Requirements: {job.requirements}
CV Content: {cv_text}

Remember:
1. Start your response with "Score: " followed by a single number (1, 2, or 3)
2. Follow with "Explanation: " and your detailed evaluation
3. Ensure there is a line break between Score and Explanation
4. Base your evaluation strictly on how well the CV matches the job requirements
5. In the explanation, clearly state which requirements are met or missing
6. Do not include any other text or formatting in your response"""

        message = self.client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text

    def extract_score(self, evaluation):
        try:
            score_line = evaluation.split('\n')[0]
            return int(score_line.split(':')[1].strip())
        except:
            return 0
