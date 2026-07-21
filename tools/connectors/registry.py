
class ConnectorRegistry:
    def __init__(self):
        self.connectors = {}
        
    def register(self, name, connector_class):
        self.connectors[name] = connector_class()
        
    def get_connector(self, name):
        return self.connectors.get(name)

    def get_all(self):
        return self.connectors

registry = ConnectorRegistry()
