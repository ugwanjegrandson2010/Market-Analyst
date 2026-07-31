class ReportFormatter:

    def format(
            self, 
            report
    ):
        
        return {
            "title":report.title,
            "summary":report.summary,
            "recommendation": report.recommendation,
            "confidence": report.confidence,
            "reasons": report.reasons,
            "risks":report.risks
        }

    