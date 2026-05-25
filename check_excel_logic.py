import openpyxl
import pandas as pd

# We need to ensure that the "Pastoreo" and other sheets correctly reference the 3 sections.
# If they use Pivot Tables or fixed ranges, they might need adjustment.
# Let's check "kg MS" sheet.

df_kg_ms = pd.read_excel('Plan de pastoreo.xlsx', sheet_name='kg MS')
print("kg MS columns:", df_kg_ms.columns.tolist())
print("kg MS unique IDs:", df_kg_ms['id'].unique() if 'id' in df_kg_ms.columns else "No ID column")
