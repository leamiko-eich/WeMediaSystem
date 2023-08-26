use wemedia;
CREATE TABLE table_target_user (
    platform VARCHAR(100),
    content_category VARCHAR(100),
    author VARCHAR(100), 
    is_scrawl TINYINT,
    last_scrawl_time DATETIME,
    subscribe_link VARCHAR(200),
    is_scrawl_success TINYINT,
    fail_reason VARCHAR(200)
);