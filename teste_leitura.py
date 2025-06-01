from s3_reader import carregar_csv_do_s3

df = carregar_csv_do_s3()
if df is not None:
    print(df.head())
