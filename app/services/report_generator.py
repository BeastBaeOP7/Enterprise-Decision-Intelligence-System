import json
import os
from datetime import datetime
from app.utils.logger import logger

class ReportGenerator:
    def __init__(self):
        self.reports_path = os.getenv("REPORTS_PATH", "./data/reports")
        os.makedirs(self.reports_path, exist_ok=True)

    def generate_json_report(self, data: dict, filename: str = None) -> str:
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.reports_path, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Report generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""

    def generate_markdown_report(self, content: str, filename: str = None) -> str:
        if not filename:
            filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        filepath = os.path.join(self.reports_path, filename)
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            logger.info(f"Markdown report generated: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return ""

report_generator = ReportGenerator()
