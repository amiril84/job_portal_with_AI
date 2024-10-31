import pandas as pd
from io import BytesIO
from datetime import datetime

class ExcelGenerator:
    @staticmethod
    def generate_candidates_excel(candidates, is_shortlisted=False):
        data = []
        for candidate in candidates:
            data.append({
                'Full Name': candidate.full_name,
                'Email': candidate.email,
                'Job Title': candidate.job.title,
                'Location': candidate.job.location,
                'Score': candidate.score,
                'Evaluation': candidate.evaluation,
                'Application Date': candidate.applied_at.strftime('%Y-%m-%d'),
                'Status': 'Shortlisted' if candidate.is_shortlisted else 'Applied'
            })
        
        df = pd.DataFrame(data)
        
        # Create Excel writer object
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Candidates', index=False)
            
            # Get workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets['Candidates']
            
            # Add formats
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4B0082',
                'font_color': 'white'
            })
            
            # Format the header row
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(col_num, col_num, 15)
            
            # Set evaluation column width
            worksheet.set_column('F:F', 40)
        
        return output.getvalue()