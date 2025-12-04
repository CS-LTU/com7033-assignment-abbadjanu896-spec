# AI DISCLOSURE STATEMENT

## Assessment Requirement Compliance

As required by the COM7033 Secure Software Development module assessment brief, this document provides a declaration of generative AI usage in the completion of this assignment.

---

## AI Usage Declaration

**This assignment used generative AI in the following ways for the purposes of completing the assignment:**

1. **Brainstorming** - Exploring potential security features and application architecture approaches
2. **Research** - Understanding Flask security best practices and OWASP guidelines
3. **Planning** - Structuring project components and development workflow
4. **Feedback** - Code review assistance and identifying potential security vulnerabilities
5. **Editing** - Improving code documentation and refining error messages

---

## AI Tools Used

- **GitHub Copilot** - Code completion and suggestions for boilerplate code
- **ChatGPT/Claude** - Technical documentation review and security best practice guidance

---

## Evidence of AI Usage

### Example Interactions:

1. **Security Implementation Query**
   - Prompt: "What are the best practices for implementing CSRF protection in Flask applications?"
   - Used for: Understanding and implementing Flask-WTF CSRF tokens

2. **Database Architecture**
   - Prompt: "When should I use dual database architecture (SQLite + MongoDB) for a web application?"
   - Used for: Planning the separation of user authentication and patient data storage

3. **Password Hashing**
   - Prompt: "What is the recommended password hashing method in Werkzeug Security?"
   - Used for: Implementing PBKDF2-SHA256 password hashing in the User model

4. **Input Validation**
   - Prompt: "How to prevent SQL injection in Flask with SQLAlchemy?"
   - Used for: Understanding ORM benefits and implementing secure queries

5. **Testing Strategy**
   - Prompt: "What are essential unit tests for authentication systems?"
   - Used for: Structuring the test suite in tests/ directory

---

## Personal Contribution Statement

While generative AI tools were used for guidance, research, and feedback:

- **All code was written and understood personally**
- **Security implementations were tested and verified independently**
- **Project architecture decisions were made based on understanding, not blind copying**
- **All debugging and problem-solving was performed personally**
- **Database design and model relationships were created independently**

The AI tools served as **learning aids and research assistants**, similar to consulting documentation, Stack Overflow, or textbooks. The final implementation reflects personal understanding and application of secure software development principles.

---

## Academic Integrity Declaration

I confirm that:

1. I understand how all the code in this project works
2. I can explain every security feature implemented
3. I have not submitted AI-generated code without understanding it
4. All work submitted is my own, with AI used only as a learning tool
5. I am prepared to demonstrate and explain any part of this project

---

## Specific AI-Assisted Components

### Components where AI provided guidance:

1. **Flask-WTF Form Validation Structure** - AI suggested validator patterns, I implemented specific business logic
2. **Security Headers Configuration** - AI listed recommended headers, I researched and applied them appropriately
3. **MongoDB Connection Handling** - AI provided error handling patterns, I adapted to project needs
4. **Logging Configuration** - AI suggested rotating file handlers, I customized for security event tracking
5. **Unit Test Structure** - AI showed pytest patterns, I wrote specific test cases for the application

### Components developed independently:

1. Patient data model and all CRUD operations
2. User authentication flow and session management
3. All route handlers and business logic
4. HTML templates and UI design
5. Database schema design and indexing strategy
6. Error handling and custom error pages
7. Security event logging system
8. Input sanitization functions

---

## Learning Outcomes Achieved

Through this project, with AI as a learning assistant, I have demonstrated:

✅ Understanding of secure programming concepts and techniques
✅ Ability to manipulate and analyze data using Python libraries
✅ Awareness of ethical, secure, and professional software development
✅ Skills to develop technical solutions for complex problems
✅ Proficiency in Flask, SQLAlchemy, MongoDB, and security frameworks
✅ Knowledge of OWASP Top 10 and security best practices

---

**Date:** December 4, 2025

**Module:** COM7033 - Secure Software Development

**Assessment:** Software Artefact (70% weighting)

---

**Note:** This disclosure is provided in accordance with university academic integrity policies and the specific requirements outlined in the assessment brief dated October 20, 2025.
