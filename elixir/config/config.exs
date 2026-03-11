import Config

if Mix.env() == :test do
  config :junit_formatter,
    report_dir: "reports",
    report_file: "exunit-results.xml"
end
