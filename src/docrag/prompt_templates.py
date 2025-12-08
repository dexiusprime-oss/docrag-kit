"""Prompt template management for DocRAG Kit."""

# Predefined prompt templates for different project types

SYMFONY_TEMPLATE = """You are an expert in Symfony PHP framework and related technologies.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide code examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:"""

IOS_TEMPLATE = """You are an expert in iOS development with Swift, UIKit, SwiftUI, and iOS SDK.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide code examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:"""

GENERAL_TEMPLATE = """You are a helpful developer assistant.
Use the following context from the project documentation to answer the question.

Rules:
- Answer precisely based on the provided context
- If information is not in the context, say so honestly
- Provide examples when relevant
- Support both Russian and English in questions and answers
- Keep technical terms and code in original language

Context:
{context}

Question: {question}

Answer:"""


class PromptTemplateManager:
    """Manages prompt templates for different project types."""
    
    TEMPLATES = {
        "symfony": SYMFONY_TEMPLATE,
        "ios": IOS_TEMPLATE,
        "general": GENERAL_TEMPLATE,
        "custom": GENERAL_TEMPLATE  # Default to general for custom
    }
    
    @staticmethod
    def get_template(project_type: str) -> str:
        """
        Get prompt template for project type.
        
        Args:
            project_type: Type of project (symfony, ios, general, custom).
        
        Returns:
            Prompt template string.
        """
        return PromptTemplateManager.TEMPLATES.get(project_type, GENERAL_TEMPLATE)
    
    @staticmethod
    def create_custom_template(template: str) -> str:
        """
        Validate and return custom template.
        
        Args:
            template: Custom template string.
        
        Returns:
            Validated template string.
        
        Raises:
            ValueError: If template is missing required placeholders.
        """
        required_placeholders = ['{context}', '{question}']
        for placeholder in required_placeholders:
            if placeholder not in template:
                raise ValueError(f"Template must contain {placeholder} placeholder")
        
        return template
