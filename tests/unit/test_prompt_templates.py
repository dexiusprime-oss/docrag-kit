"""Unit tests for prompt templates."""

import pytest
from docrag.prompt_templates import (
    SYMFONY_TEMPLATE,
    IOS_TEMPLATE,
    GENERAL_TEMPLATE,
    get_template_for_project_type
)


class TestPromptTemplates:
    """Test prompt template definitions."""
    
    def test_symfony_template_structure(self):
        """Test Symfony template has required placeholders."""
        assert "{context}" in SYMFONY_TEMPLATE
        assert "{question}" in SYMFONY_TEMPLATE
        assert "Symfony" in SYMFONY_TEMPLATE or "symfony" in SYMFONY_TEMPLATE.lower()
    
    def test_ios_template_structure(self):
        """Test iOS template has required placeholders."""
        assert "{context}" in IOS_TEMPLATE
        assert "{question}" in IOS_TEMPLATE
        assert "iOS" in IOS_TEMPLATE or "ios" in IOS_TEMPLATE.lower()
    
    def test_general_template_structure(self):
        """Test general template has required placeholders."""
        assert "{context}" in GENERAL_TEMPLATE
        assert "{question}" in GENERAL_TEMPLATE
    
    def test_templates_are_strings(self):
        """Test all templates are strings."""
        assert isinstance(SYMFONY_TEMPLATE, str)
        assert isinstance(IOS_TEMPLATE, str)
        assert isinstance(GENERAL_TEMPLATE, str)
    
    def test_templates_not_empty(self):
        """Test templates are not empty."""
        assert len(SYMFONY_TEMPLATE) > 0
        assert len(IOS_TEMPLATE) > 0
        assert len(GENERAL_TEMPLATE) > 0


class TestGetTemplateForProjectType:
    """Test template selection by project type."""
    
    def test_get_symfony_template(self):
        """Test getting Symfony template."""
        template = get_template_for_project_type("symfony")
        assert template == SYMFONY_TEMPLATE
    
    def test_get_ios_template(self):
        """Test getting iOS template."""
        template = get_template_for_project_type("ios")
        assert template == IOS_TEMPLATE
    
    def test_get_general_template(self):
        """Test getting general template."""
        template = get_template_for_project_type("general")
        assert template == GENERAL_TEMPLATE
    
    def test_get_custom_template_returns_general(self):
        """Test custom type returns general template."""
        template = get_template_for_project_type("custom")
        assert template == GENERAL_TEMPLATE
    
    def test_get_unknown_template_returns_general(self):
        """Test unknown type returns general template."""
        template = get_template_for_project_type("unknown")
        assert template == GENERAL_TEMPLATE
    
    def test_case_insensitive_template_selection(self):
        """Test template selection is case insensitive."""
        template1 = get_template_for_project_type("SYMFONY")
        template2 = get_template_for_project_type("symfony")
        assert template1 == template2
