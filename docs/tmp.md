## Return Values

| Name        | Values |
| ----        | ------ |
| ReturnValue | This is the status of GetRemoteServicesAPIStatus not the status of the iDRAC/Server.  <ul><li>0 = Request was successfully executed</li><li>1 = Error occurred</li></ul> |
| Status      | The overall status of the Remote Services API. This tells you if the iDRAC is ready to receive commands.  <ul><li>0 = Ready</li><li>1 = Not Ready</li></ul> |
| LCStatus    | The Lifecycle Controller status that includes the Data Manager status.  <ul><li>0 = Ready</li><li>1 = Not Initialized</li><li>2 = Reloading Data</li><li>3 = Disabled</li><li>4 = In Recovery</li><li>5 = In Use</li><li></ul> |
