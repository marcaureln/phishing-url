SELECT COUNT(id)                                       AS total_url,
       COUNT(CASE WHEN is_phishing = TRUE THEN 1 END)  AS total_phishing,
       COUNT(CASE WHEN is_phishing = FALSE THEN 1 END) AS total_legitimate,
       COUNT(CASE WHEN is_online = TRUE THEN 1 END)    AS total_online
FROM url;