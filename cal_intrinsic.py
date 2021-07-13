def sort_df_intrinsic(df_intrinsic, df_xyz):
    df_intrinsic = df_intrinsic.reindex(index=df_xyz.index)
    return df_intrinsic