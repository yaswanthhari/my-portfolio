import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import summarize
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from summarize import AISummarizer

@pytest.fixture
def mock_summarizer():
    with patch('summarize.AutoTokenizer.from_pretrained') as mock_tok, \
         patch('summarize.AutoModelForSeq2SeqLM.from_pretrained') as mock_mod:
        
        # Mock tokenizer behaviors
        mock_tokenizer_instance = MagicMock()
        mock_tokenizer_instance.return_value = {"input_ids": "mock_ids"}
        mock_tokenizer_instance.decode.return_value = "This is a mock summary."
        mock_tok.return_value = mock_tokenizer_instance
        
        # Mock model behaviors
        mock_model_instance = MagicMock()
        mock_model_instance.generate.return_value = [["mock_summary_id"]]
        mock_mod.return_value = mock_model_instance
        
        summarizer = AISummarizer(model_name="fake-model")
        yield summarizer, mock_tokenizer_instance, mock_model_instance

def test_summarize_logic(mock_summarizer):
    summarizer, mock_tok, mock_mod = mock_summarizer
    
    text = "This is a long text that needs summarization. " * 50
    result = summarizer.summarize(text)
    
    # Assert model was called
    mock_mod.generate.assert_called_once()
    assert result == "This is a mock summary."

def test_get_text_from_file(tmp_path, mock_summarizer):
    summarizer, _, _ = mock_summarizer
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("Hello World!")
    
    assert summarizer.get_text_from_file(test_file) == "Hello World!"

def test_get_text_file_not_found(mock_summarizer):
    summarizer, _, _ = mock_summarizer
    
    with pytest.raises(FileNotFoundError):
        summarizer.get_text_from_file(Path("does_not_exist.txt"))
