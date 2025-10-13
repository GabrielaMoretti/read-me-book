# Requirements Update Documentation

## Changes Made

### Updated Core Dependencies

1. **pypdf** (formerly PyPDF2)
   - Changed from: `PyPDF2==3.0.1`
   - Changed to: `pypdf>=4.0.0`
   - Reason: PyPDF2 was renamed to pypdf, and version 4.0+ includes improvements and bug fixes

2. **pdfplumber**
   - Changed from: `pdfplumber==0.10.3`
   - Changed to: `pdfplumber>=0.10.0`
   - Reason: Using >= for flexibility while maintaining compatibility

3. **pyttsx3**
   - Changed from: `pyttsx3==2.90`
   - Changed to: `pyttsx3>=2.90`
   - Reason: Allow newer versions with bug fixes

4. **Pillow**
   - Changed from: `pillow==10.1.0`
   - Changed to: `Pillow>=10.0.0`
   - Reason: Standardized capitalization and allow updates

### New Web Framework Dependencies

Added support for future web version development:

1. **Flask** (`Flask>=3.0.0`)
   - Main web framework option
   - Production-ready for web applications

2. **Flask-CORS** (`Flask-CORS>=4.0.0`)
   - Cross-Origin Resource Sharing support
   - Required for API access from different domains

3. **Flask-SQLAlchemy** (`Flask-SQLAlchemy>=3.0.0`)
   - Flask integration with SQLAlchemy
   - Simplifies database operations in Flask

### Database Support

4. **SQLAlchemy** (`SQLAlchemy>=2.0.0`)
   - ORM for database operations
   - Enables saving notes, chapters, and user preferences

### Alternative API Framework

5. **FastAPI** (`fastapi>=0.100.0`)
   - Modern, fast API framework
   - Alternative to Flask for API development

6. **uvicorn[standard]** (`uvicorn[standard]>=0.23.0`)
   - ASGI server for FastAPI
   - Includes extra dependencies for production use

7. **pydantic** (`pydantic>=2.0.0`)
   - Data validation using Python type annotations
   - Required by FastAPI

### Utilities

8. **python-dotenv** (`python-dotenv>=1.0.0`)
   - Environment variable management
   - Helps manage configuration securely

## Installation

To install all dependencies:

```bash
pip install -r requirements.txt
```

To install only core dependencies (for desktop app):

```bash
pip install pypdf pdfplumber pyttsx3 Pillow
```

To install web development dependencies:

```bash
pip install Flask Flask-CORS Flask-SQLAlchemy SQLAlchemy
```

To install API development dependencies:

```bash
pip install fastapi uvicorn[standard] pydantic
```

## Compatibility

- All changes maintain backward compatibility with existing code
- The desktop application (audiobook_app.py) will work with updated dependencies
- New dependencies are for future web version features
- Using `>=` versioning allows flexibility while maintaining minimum requirements

## Future Development

The updated requirements.txt prepares the project for:

1. **Web Version**: Browser-based interface using Flask or FastAPI
2. **Notes & Bookmarks**: Persistent storage of user annotations
3. **User Accounts**: Optional user management system
4. **Cloud Deployment**: Ready for hosting on web platforms
5. **API Access**: RESTful API for programmatic access

## Notes

- The original application only imported `pdfplumber` and `pyttsx3`
- PyPDF2 was listed but never actually imported in the code
- Web framework dependencies are added in preparation for future features
- All documentation files have been updated to reflect these changes
