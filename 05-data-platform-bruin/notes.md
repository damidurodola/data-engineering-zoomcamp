Module 5: Data Platforms

Bruin is a data platform that helps to manage the entire data lifecycle from ingestion to analytics. It contains the following tools:
- Data ingestion (extract data from source to warehouse)
- Data transformation ( clean, model and aggregate data)
- Data orchestration ( schedule and manage dependency)
- Data quality (built-in checks and validation)
- Metadata management (lineage and documentation)

How to install Bruin
Via CLI:
```
curl -LsSf https://getbruin.com/install/cli | sh
OR
wget -qO- https://getbruin.com/install/cli | sh
```
Then install the Bruin extension for VSCode or Cursor.

Bruin MCP
Bruin provides an MCP (Model Context Protocol) server that you can add to your IDE to use AI agents for creating pipelines.
VSCode
- Open the command paleette in VS Code (`Cmd+Shift+P`)
- Run `MCP:Add Server` command
- Choode `Command stdio` as the transport type
- Enter `bruin mcp` as the command.
- Restart your IDE to complete the setup.

Initialize a Bruin project
`bruin init `
