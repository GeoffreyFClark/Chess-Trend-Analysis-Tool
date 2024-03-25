# Oracle-Flask Setup 
## To access database: 
1. Navigate to backend directory

`cd python-backend`

2. Start virtual environment

`venv\Scripts\activate` (On Mac: `source venv/bin/activate`)

3. Reinstall requirements (oracledb added)

`pip install -r requirements.txt` 

  OR install oracledb directly

`pip install oracledb`

4. Navigate to https://www.oracle.com/database/technologies/instant-client.html and install Oracle client

5. Add Oracle client path as a system variable within environment variables.

  Important: Name this system variable ORACLE_HOME.

  Windows: System->About->Advanced system settings->Environment Variables->Add New in System Variables

NOTE that usage of OracleDB via a UF account requires an active Gatorlink VPN connection.