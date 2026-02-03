# Demo-ATS
This FastAPI backend serves as a versatile, branch-agnostic resume analyzer designed to handle both PDF and DOCX formats without persistent storage. It is architected to transition from a general structural evaluator into a high-fidelity ATS (Applicant Tracking System) scorer by leveraging memory-efficient parsing. 

Project Overview
The system currently provides an objective quality score by analyzing universal professional markers, such as:


    Structural Integrity: Validates the presence of essential sections like Education, Experience, and Skills.



    Quantifiable Impact: Detects numerical achievements, such as your 8.33 CGPA or the 50+ students you mentored, which are vital for both technical and non-technical roles.



    Action-Oriented Language: Identifies strong verbs like "Engineered," "Organized," and "Automated" to gauge professional authority.


    Contactability: Ensures recruiters can reach the candidate via email, phone, or professional links like LinkedIn and GitHub.


Future Scalability
The codebase is structured to evolve into a job-description-matching engine:

    JD Comparison: Future modules can implement cosine similarity or NLP to compare the parsed resume text against specific job descriptions to calculate a "Relevancy Score."


    Multi-Format Support: By using PyMuPDF and python-docx, it ensures a consistent data stream regardless of whether the user is a Data Science student or a creative professional.



    Mobile Integration: Optimized for Kotlin-based mobile applications, providing clear, actionable "Areas for Improvement" to help users optimize their resumes before submission.
