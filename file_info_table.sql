CREATE TABLE file_info(
    id INT IDENTITY(1,1) PRIMARY KEY,
    path NVARCHAR(MAX),      -- 文件路徑
    operation NVARCHAR(MAX),  -- 執行操作的結果，例如從Python腳本中返回的 'transpose' 或 'Error'
    pattern NVARCHAR(MAX),
    start_index INT,
    end_index INT,
    transformed_new_path NVARCHAR(MAX) DEFAULT N'None'
);


