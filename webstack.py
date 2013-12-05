import dockyard

cli = dockyard.Cli()
cli.addPlugin(dockyard.DockerPlugin())
cli.addPlugin(dockyard.DockyardPlugin())
cli.addPlugin(dockyard.StackPlugin())
cli.parse()