import pandas as pd
import pyodbc
import getpass
from tkinter import *
from tkinter import filedialog
from easygui import passwordbox
from Flask.Client import Client


class RNPD:
    def __init__(self, driver, server, db, user, pwd, *args, **kwargs):
        self.conn = pyodbc.connect(driver=driver,
                                   server=server,
                                   database=db,
                                   uid=user,
                                   pwd=pwd,
                                   )
        self.header = ['a1',
                       'a2',
                       'a3',
                       'a4',
                       'a5',
                       'a6',
                       'a7',
                       'a8',
                       'a9',
                       'a10',
                       'a11',
                       'a12',
                       'a13',
                       'a14',
                       'a15',
                       'a16',
                       'a17',
                       'a18',
                       'a19',
                       'a20',
                       'a21',
                       'a22',
                       'a23',
                       'a24',
                       'a25',
                       'a26',
                       'a27',
                       'a28',
                       'a29',
                       'a30',
                       'a31',
                       'a32',
                       'a33',
                       'a34',
                       'a35',
                       'a36',
                       'a37',
                       'a38',
                       'a39',
                       'a40',
                       'SortOrder',
                       'rowcreated',
                       'rowupdated',
                       'userupdated',
                       'id',
                       'source']
        self.cursor = self.conn.cursor()


    def Main(self):
        self.datainput()
        self.newproducts()
        self.newcustomers()
        self.productdups()
        self.customerdups()
        self.updatetable()
        self.clearconfig()

    ########################################################################################################################

    def cli_name(self, client):
        return client


    def datainput(self):
        """Gets AA Table from Radar and loads NPD spreadsheet"""
        querystring = "SELECT * FROM dbo.AllowableAttributes"
        self.aa = pd.read_sql(querystring, self.conn)
        # self.prodref['Material'] = self.prodref['Material'].astype(str)

        print('Please select the NPD file')
        self.xls = pd.ExcelFile(filedialog.askopenfilename())

    def newproducts(self):
        """Defines product dataframe and validates format"""
        self.proddf = pd.read_excel(self.xls, sheet_name='New Products')
        if not self.proddf.empty():
            pass
        else:
            print("No new products were loaded.")
        if self.header == list(self.proddf):
            pass
        else:
            raise AssertionError("Product headers do not match!")

    def newcustomers(self):
        """Defines customer dataframe and validates format"""
        self.custdf = pd.read_excel(self.xls, sheet_name='New Customers')
        if not self.custdf.empty():
            pass
        else:
            print("No new customers were loaded.")
        if self.header == list(self.custdf):
            pass
        else:
            raise AssertionError("Customer headers do not match!")

    def productdups(self):
        """Extracts any duplicate product values and asks the user to save in a new .csv file """
        if not self.proddf.empty():
            prodcheck = pd.concat([self.aa, self.proddf])
            dups = prodcheck[prodcheck.duplicated(subset=['a4', 'a30'], keep='last')]
            checkcount = len(dups.index)

            if checkcount > 1:
                print("Alert! " + str(
                    checkcount) + " Duplicate products identified. Please choose a file location and review duplicate products.")
                path_to = filedialog.asksaveasfilename(title="Save file", defaultextension=".csv",
                                                       filetype=[("CSV file", "*.csv")])
                return dups.to_csv(path_to)
            else:
                pass
        else:
            pass

    def customerdups(self):
        """Extracts any duplicate customer values and asks the user to save in a new .csv file """

        dupfields = ['a4', 'a5', 'a6', 'a7', 'a8', 'a9']
        if not self.custdf.empty():
            custcheck = pd.concat([self.aa, self.custdf])
            dups = custcheck[custcheck.duplicated(subset=dupfields, keep='last')]
            checkcount = len(dups.index)

            # implement check to see if the same customer exists with a different channel (channel is either a5 or a6.) if a4 and a7 is duplicated, check a5 or a6

            if checkcount > 1:
                print("Alert! " + str(
                    checkcount) + " Duplicate customers identified. Please choose a file location and review duplicate products.")
                path_to = filedialog.asksaveasfilename(title="Save file", defaultextension=".csv",
                                                       filetype=[("CSV file", "*.csv")])
                return dups.to_csv(path_to)
            else:
                pass
        else:
            pass

    def updatetable(self):
        """Send NPD to Allowable Attributes table"""
        self.proddf.to_sql('dbo.AllowableAttributes', self.conn, index=False, if_exists='append')

    def clearconfig(self):
        """Clear Config tables and rerun Staging process"""
        self.cursor.execute("DELETE FROM [Config].[Products]")
        self.cursor.execute("DELETE FROM [Config].[Customers]")
        self.cursor.execute("EXEC [Staging].[ExecuteAllInOrder]")
        self.cursor.commit()


# for everyone except Matrix, need to check a19 to see if that value already exists in AA. If new, flag, if its new, need to add AS and BSR

pwd = passwordbox("Enter Password: ")
user = getpass.getuser()

client_list = {
    'Django': (r'{ODBC Driver 13 for SQL Server};', r'danone-uat.acumenci.com;',
               r'Django_UAT_Radar;', user, r'{};'.format(pwd)),

    'Elektra': (r'{ODBC Driver 13 for SQL Server};', r'dog.acumenci.com;',
                r'Elektra_Live_Radar;', user, r'{};'.format(pwd)),

    'Highlander': (r'{ODBC Driver 13 for SQL Server};', r'hnkn.acumenci.com;',
                   r'Highlander_Live_Radar;', user, r'{};'.format(pwd)),

    'Matrix': (r'{ODBC Driver 13 for SQL Server};', r'mae.acumenci.com;',
               r'Matrix_Live_Radar;', user, r'{};'.format(pwd))
}

if __name__ == '__main__':
    root = Tk()
    clientname = RNPD.cli_name(Client(root))
    RNPD(*client_list[clientname]).Main()
