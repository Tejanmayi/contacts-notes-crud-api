from typing import Dict, Any, Optional
import re

class FieldNormalizer:
    """Utility class for normalizing field names and values in notes."""
    
    # Common field name mappings
    FIELD_MAPPINGS = {
        'content': ['body', 'text', 'message', 'note', 'description', 'notes', 'note_content', 'note_description', 'note_notes', 'note_text', 'note_message'],
        'contact_id': ['contact', 'contactId', 'contact_id', 'person_id', 'personId', 'id', 'Id'],
    }
    
    @classmethod
    def normalize_field_name(cls, field_name: str) -> str:
        """Normalize a field name to a standard format.
        
        Args:
            field_name: The field name to normalize
            
        Returns:
            The normalized field name
        """
        # Convert to lowercase and replace spaces/underscores with nothing
        normalized = re.sub(r'[_\s]', '', field_name.lower())
        
        # Check if the normalized name matches any of our known field mappings
        for standard_name, variations in cls.FIELD_MAPPINGS.items():
            if normalized in variations or normalized == standard_name:
                return standard_name
                
        return field_name
    
    @classmethod
    def normalize_note_data(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize note data by standardizing field names.
        
        Args:
            data: The note data to normalize
            
        Returns:
            Dictionary with normalized field names
        """
        normalized = {}
        
        for key, value in data.items():
            normalized_key = cls.normalize_field_name(key)
            normalized[normalized_key] = value
            
        return normalized
    
    @classmethod
    def validate_required_fields(cls, data: Dict[str, Any]) -> Optional[str]:
        """Validate that required fields are present in the data.
        
        Args:
            data: The note data to validate
            
        Returns:
            Error message if validation fails, None if validation passes
        """
        required_fields = {'content', 'contact_id'}
        missing_fields = required_fields - set(data.keys())
        
        if missing_fields:
            return f"Missing required fields: {', '.join(missing_fields)}"
            
        return None 