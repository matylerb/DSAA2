import pandas as pd
import numpy as np
from ydata_profiling import ProfileReport

#really cool library for exploring data, that I found on Instagram
df = pd.read_csv("data/movies.csv")   

#instantly creates a html report
profile = ProfileReport(df, title="Movies Exploration Report", explorative=True)

profile.to_file("movies_report.html")