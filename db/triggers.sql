-- Function to auto-update updated_at columns
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for `source` table
CREATE TRIGGER update_source_updated_at
BEFORE UPDATE ON source
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

-- Trigger for `url` table
CREATE TRIGGER update_url_updated_at
BEFORE UPDATE ON url
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();