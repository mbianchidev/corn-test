defmodule CornTest.MixProject do
  use Mix.Project

  def project do
    [
      app: :corn_test,
      version: "1.0.0",
      elixir: "~> 1.16",
      start_permanent: Mix.env() == :prod,
      deps: deps()
    ]
  end

  def application do
    [extra_applications: [:logger]]
  end

  defp deps do
    [
      {:junit_formatter, "~> 3.3", only: :test}
    ]
  end
end
