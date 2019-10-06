import sqlite3
import ipywidgets
import pandas
import os
from IPython.display import display, display_markdown

class parser():
    tableStyle = '''
        <style>
        .sqltable td,th { padding: 4px; }
        .sqltable th { background-color: skyblue; text-align: center;}
        .sqltable td { text-align: right; }
        .sqltable tr:hover {background-color: #e0e0e0}
        </style>
        <div style="padding: 10px 72px 20px;">
        %s
        </div>'''
    errorStyle = '<p style="margin-left: 72px;"><span style="color: red;">SQL Error:</span> %s</p>'
    schemaStyle = '<p style="margin: 0px 72px; line-height: 20px;">%s</p>'
    defaultStyle = '<p style="margin: 10px 72px;"><strong>%s<strong></p>'
    getSchema = "SELECT name, sql FROM sqlite_master WHERE type='table' OR type='view' ORDER BY name"
    getTable = "SELECT name, sql FROM sqlite_master WHERE name='%s'"

    def __init__(self, dbfilename, initialize='', mode='r', output='html'):
        """
            Generates an interactive SQL interface for interacting with
            the given sqlite3 file "dbfilename". The 'mode' argument should
            be 'r' to open an existing database, 'w' to create a new one,
            or 'm' to create an in-memory database. The 'output' argument
            can be set to either 'html' or 'text'.
        """
        if (output.lower() in ['html', 'text']):
            self.output = output.lower()
        else:
            print('Unsupported output format: "%s", use one of "html" or "text"' % output)
        self.result = None
        self.history = []
        self.histIdx = 0
        buttonRow = []
        self.query = ipywidgets.Textarea(description="SQL:", value=initialize, 
                                         layout=ipywidgets.Layout(width="600px", height="100px", font_weight="bold"))
        self.query.color = "#000040"

        self.executeButton = ipywidgets.Button(description="Execute")
        self.executeButton.width = "100px"
        self.executeButton.margin = "10px 5px 10px 72px"
        self.executeButton.on_click(self.executeSQL)
        buttonRow.append(self.executeButton)
        
        self.submitButton = ipywidgets.Button(description="Submit")
        self.submitButton.width = "100px"
        self.submitButton.margin = "10px 5px 10px 72px"
        self.submitButton.on_click(self.executeSQL)
        buttonRow.append(self.submitButton)
        
        self.prevButton = ipywidgets.Button(description="prev")
        self.prevButton.width = "50px"
        self.prevButton.margin = "10px 5px"
        self.prevButton.on_click(self.prevQuery)
        buttonRow.append(self.prevButton)
        
        self.nextButton = ipywidgets.Button(description="next")
        self.nextButton.width = "50px"
        self.nextButton.margin = "10px 5px"
        self.nextButton.visible = False
        self.nextButton.on_click(self.nextQuery)
        buttonRow.append(self.nextButton)

        if (self.output.lower() == 'html'):
            self.status = ipywidgets.HTML()

        self.container = ipywidgets.VBox(children=[self.query, ipywidgets.HBox(children=buttonRow), self.status])
        if isinstance(dbfilename, sqlite3.Connection):
            self.db = dbfilename
            if (self.output == 'html'):
                self.status.value = 'Using existing database connection'
            else:
                print('Using existing database connection')
        elif ('r' in mode) and os.path.isfile(dbfilename):
            self.db = sqlite3.connect(dbfilename)
            if (self.output == 'html'):
                self.status.value = 'Connected to database: <em>&quot;%s&quot;</em>' % dbfilename
            else:
                print('Connected to database: "%s"' % dbfilename)
        elif ('w' in mode):
            if os.path.isfile(dbfilename):
                os.remove(dbfilename)
            self.db = sqlite3.connect(dbfilename)
            if (self.output == 'html'):
                self.status.value = 'Created database: <em>&quot;%s&quot;</em>' % dbfilename
            else:
                print('Created database: "%s"' % dbfilename)
        else:
            if (self.output == 'html'):
                self.status.value = self.errorStyle % ("Database &quot;%s&quot; does not exist" % dbfilename)
            else:
                print('Connected to database: "%s"' % dbfilename)
            self.query.close()
            self.submitButton.close()
        display(self.container)

    def executeSQL(self, button):
        """
            Excutes 'query' in textarea in respose to the 'submit' button. Either
            the 'status' div or the cell's output region are updated according to
            whether the output mode is set to 'html' or 'text'. An explict COMMIT
            is required to modify a database file opened in either 'r' or 'w' mode.
            The pseudo command ".schema" dumps the database's schema, and '.changes'
            gives the total number of changes to the database in this interactive
            session.
        """
        query = self.query.value
        self.history.append(query)
        self.histIdx = -1
        if (query.strip().lower().startswith('.schema')):
            table = query[7:].strip()
            if len(table):
                df = pandas.read_sql_query(self.getTable % table, self.db)
            else:
                df = pandas.read_sql_query(self.getSchema, self.db)
            if (self.output == 'html'):
                html = ''
            for i, sql in enumerate(df['sql']):
                if not (df['name'][i].startswith('sqlite_')):
                    if (self.output == 'html'):
                        html += self.schemaStyle % (sql.replace(' ', '&nbsp;').replace('\n', '<br>'))
                    else:
                        print(sql)
                        print()
            if (self.output == 'html'):
                self.status.value = '<div class="sqldiv">%s</div>' % html
            self.result = None
            return
        if (query.strip().lower() == '.changes'):
            if (self.output == 'html'):
                self.status.value = self.defaultStyle % ("SQL Total Changes = %d" % self.db.total_changes)
            else:
                print("SQL Total Changes = %d" % self.db.total_changes)
            self.result = None
            return
        elif (query.strip().lower() == 'commit'):
            self.db.commit()
            if (self.output == 'html'):
                self.status.value = self.defaultStyle % "SQL Transaction committed"
            else:
                print("SQL Transaction committed")
            self.result = None
            return
        try:
            df = pandas.read_sql_query(query, self.db)
            if (self.output == 'html'):
                result = df.to_html(max_rows=50, classes='sqltable')
                self.status.value = self.tableStyle % result
            else:
                print(df)
                print()
            self.result = [[v for v in row.values] for i, row in df.iterrows()]
        except TypeError as error:
            if (self.output == 'html'):
                self.status.value = self.defaultStyle % "SQL Command Succeeded"
            else:
                print("SQL Command Succeeded")
            pass
            self.result = None
        except Exception as error:
            if (self.output == 'html'):
                self.status.value = self.errorStyle % str(error)
            else:
                print("SQL Error: %s" % str(error))
            pass
            self.result = None

    def prevQuery(self, button):
        if (len(self.history) + self.histIdx > 0):
            self.histIdx -= 1
            self.query.value = self.history[self.histIdx]
            self.nextButton.visible = True

    def nextQuery(self, button):
        if (self.histIdx < 0):
            self.histIdx += 1
            self.query.value = self.history[self.histIdx]
            self.nextButton.visible = (self.histIdx < -1)
