-- Create dashboards table
CREATE TABLE IF NOT EXISTS dashboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create data_files table to store file metadata
CREATE TABLE IF NOT EXISTS data_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_id UUID REFERENCES dashboards(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create kpi_charts table to store chart configurations
CREATE TABLE IF NOT EXISTS kpi_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_id UUID REFERENCES dashboards(id) ON DELETE CASCADE,
    chart_type VARCHAR(50) NOT NULL,
    chart_title VARCHAR(255),
    x_column VARCHAR(255),
    y_column VARCHAR(255),
    metric_column VARCHAR(255),
    config JSONB DEFAULT '{}',
    position INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create kpi_data table for storing processed KPI data
CREATE TABLE IF NOT EXISTS kpi_data (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dashboard_id UUID REFERENCES dashboards(id) ON DELETE CASCADE,
    chart_id UUID REFERENCES kpi_charts(id) ON DELETE CASCADE,
    metric_name VARCHAR(255),
    value NUMERIC,
    label VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_dashboards_created_at ON dashboards(created_at);
CREATE INDEX IF NOT EXISTS idx_data_files_dashboard_id ON data_files(dashboard_id);
CREATE INDEX IF NOT EXISTS idx_kpi_charts_dashboard_id ON kpi_charts(dashboard_id);
CREATE INDEX IF NOT EXISTS idx_kpi_data_dashboard_id ON kpi_data(dashboard_id);
CREATE INDEX IF NOT EXISTS idx_kpi_data_chart_id ON kpi_data(chart_id);

-- Enable Row Level Security (optional, adjust as needed)
ALTER TABLE dashboards ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_files ENABLE ROW LEVEL SECURITY;
ALTER TABLE kpi_charts ENABLE ROW LEVEL SECURITY;
ALTER TABLE kpi_data ENABLE ROW LEVEL SECURITY;

-- Create policies (allow all for now, adjust based on your security needs)
CREATE POLICY "Allow all operations on dashboards" ON dashboards
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on data_files" ON data_files
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on kpi_charts" ON kpi_charts
    FOR ALL USING (true);

CREATE POLICY "Allow all operations on kpi_data" ON kpi_data
    FOR ALL USING (true);

