import mysql.connector as m

n = m.Connect(
    user='root',
    password='',
    host='Localhost',
    database='AMS'
)
c = n.cursor()


def adr():
    def it():
        while True:
            iid = 'M' + input('Enter Item Code:\n' + ' =>')
            ina = input('Enter Item Name:\n' + ' => ').upper()
            co = input('Enter Company Name:\n' + ' => ').upper()
            ty = input('Enter Item Type:\n' + ' => ').upper()
            st = int(input('Enter Amount of Item in stock:\n' + ' => '))
            rt = float(input('Enter Rate of Item:\n' + ' => '))
            g = int(input('Enter GST on the Item:\n' + ' => '))
            c.execute(f"insert into items values('{iid}','{ina}','{co}','{ty}',{st},{rt},{g})")
            yn = input('Confirm changes ?(Y/N)')
            ag = input('Add more ?(Y,N)')
            if yn == 'Y' or yn == 'y':
                n.commit()
                print('Database updated :)')
            else:
                print('No changes made')
            if ag == 'Y' or ag == 'y':
                continue
            else:
                break

    def pr():
        while True:
            iid = input('Enter Item code (Format= M"N" eg. if item no. is 1 item code = M001):\n' + ' => ')
            qt = int(input('Enter quantity of Item Purchased:\n' + ' => '))
            rt = float(input('Enter Rate of Item:\n' + ' => '))
            d = input('Enter Date of Purchase (yyyy/mm/dd):\n' + ' => ')
            c.execute(f"update items set stock = stock + {qt} where icode = '{iid}'")
            # to check and add if an item is not available in items table
            c.execute(f"select * from items where icode = '{iid}';")
            k = c.fetchall()
            if k == []:
                print('No item id matched, Add item to continue :')
                ina = input('Enter Item Name:\n' + ' => ').upper()
                co = input('Enter Company Name:\n' + ' => ').upper()
                ty = input('Enter Item Type:\n' + ' => ').upper()
                rt = float(input('Enter Rate of Item:\n' + ' => '))
                g = int(input('Enter GST on the Item:\n' + ' => '))
                c.execute(f"insert into items values('{iid}','{ina}','{co}','{ty}',{qt},{rt},{g})")
            c.execute(f"insert into purchase values('{iid}',{qt},{rt},'{d}')")
            yn = input('Save changes ?(Y/N) : ')
            if yn == 'Y' or yn == 'y':
                n.commit()
                print('Database updated :)')
            else:
                print('No changes made :(')
            ag = input('Add more ?(Y/N) : ')
            if ag == 'Y' or ag == 'y':
                continue
            else:
                break

    def cu():
        while True:
            cid = input('Enter Customer code (Format= C"N" eg. if customer no. is 1 customer code = C001):\n' + ' => ')
            cn = input('Enter Customer name:\n' + ' => ').upper()
            ade = input('Enter Address of Customer (optional):\n' + ' => ').upper()
            ba = input('Enter Balance amount (if any) :\n' + ' => ')
            ph = int(input('Enter contact no. of Customer (optional):\n' + ' => '))
            c.execute(f"insert into customers values('{cid}',{cn},'{ade}',{ba},{ph})")
            yn = input('Save changes ?(Y/N) : ')
            if yn == 'Y' or yn == 'y':
                n.commit()
                print('Database updated :)')
            else:
                print('No changes made :(')
            ag = input('Add more ?(Y/N) : ')
            if ag == 'Y' or ag == 'y':
                continue
            else:
                break

    def sa():
        me = int(input('Enter Meno no.:\n' + ' => '))
        cid = input('Enter Customer code (Format= C"N" eg. if customer no. is 1 customer code = C001):\n' + ' => ')
        c.execute(f"select CUSTOMERID from customers where CUSTOMERID = '{cid}'")
        cc = c.fetchall()
        if not cc:
            print('Customer not available please add customer and try again :)')
            return
        else:
            pass
        while 1:
            iid = input('Enter Item code:\n' + ' => ')
            c.execute(f"select * from items where icode = '{iid}'")
            kl = c.fetchall()
            if iid in kl[0]:
                j = kl[0]
                rt = j[5]
                gst = j[6]
            else:
                print('Item not available in Inventory :(')
                continue
            if j[4] == 0:
                print('Item out of stock available :(')
                continue
            qty = int(input('Enter Quantity of item:\n' + ' => '))
            c.execute(f"update items set stock= stock - {qty} where icode = '{iid}'")
            gat = rt * gst / 100
            amt = rt * qty
            c.execute(f"insert into itemsold values('{me}','{iid}',{qty},{rt},{amt},{gat})")
            a = input('Add more items ? (Y/N)')
            if a == 'Y' or a == 'y':
                continue
            else:
                break
        md = input('Enter Date of Purchase (yyyy/mm/dd):\n' + ' => ')
        c.execute(f'select sum(GSTAMT) from itemsold where memono={me};')
        g = c.fetchall()
        a = g[0]
        ga = a[0]
        c.execute(f'select sum(RATE) from itemsold where memono={me};')
        lm = c.fetchall()
        k = lm[0]
        ta = k[0]
        c.execute(f"insert into sale values({me},'{md}','{cid}',{ta},{ga})")
        c.execute(f'update customers set balance = balance + {ta} + {ga} where CUSTOMERID = {cid}')
        yn = input('Save changes ?(Y/N) : ')
        if yn == 'Y' or yn == 'y':
            n.commit()
            print('Database updated :)')
        else:
            print('No changes made :(')

    def py():
        cid = input('Enter Customer code (Format= C"N" eg. if customer no. is 1 customer code = C001):\n' + ' => ')
        c.execute(f"select CUSTOMERID from customers where CUSTOMERID = '{cid}'")
        cc = c.fetchall()
        if not cc:
            print('Customer not available please add customer and try again :)')
            return
        else:
            pass
        me = int(input('Enter Meno no.:\n' + ' => '))
        pa = int(input('Enter amount paid:\n' + ' => '))
        mod = input('Enter mode of payment:\n' + ' => ')
        md = input('Enter Date of Payment (yyyy/mm/dd):\n' + ' => ')
        c.execute(f"insert into payments values('{cid}',{me},{pa},{mod},'{md}')")
        c.execute(f"update payments set balance = balance - {pa} where customerid= '{cid}'")
        yn = input('Save changes ?(Y/N) : ')
        if yn == 'Y' or yn == 'y':
            n.commit()
            print('Database updated :)')
        else:
            print('No changes made :(')

    while True:
        ia = int(input(
            'Adding Menu:\n' + ' 1)Add items\n' + ' 2)Add Customers\n' + ' 3)Add Purchase\n' + ' 4)Add Sales Data\n' + ' 5)Add Payment History of customers:\n' + ' 6)Exit\n' + ' => '))
        if ia == 1:
            it()
        if ia == 2:
            cu()
        if ia == 3:
            pr()
        if ia == 4:
            sa()
        if ia == 5:
            py()
        if ia == 6:
            c.close()
            break


def srh():
    def si():
        while 1:
            o = int(input(
                ' Search Item(s) using:\n' + '  1) Name\n' + '  2) Company\n' + '  3) Type\n' + '  4) Exit\n' + ' => '))
            if o == 1:
                nit = input('Enter Item name\n' + ' => ')
                c.execute(f"select * from items where itemname='{nit}';")
                kl = c.fetchall()
                if not kl:
                    print('No item found')
                else:
                    print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format('ICODE', 'ITEM NAME', 'COMPANY',
                                                                                   'TYPE',
                                                                                   'STOCK',
                                                                                   'RATE', 'GST'))
                    for i in kl:
                        print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format(i[0], i[1], i[2], i[3], i[4],
                                                                                       i[5], i[6]))
            if o == 2:
                cit = input('Enter Item Company name\n' + ' => ')
                c.execute(f"select * from items where company='{cit}';")
                kl = c.fetchall()
                if not kl:
                    print('No item found')
                else:
                    print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format('ICODE', 'ITEM NAME', 'COMPANY',
                                                                                   'TYPE',
                                                                                   'STOCK',
                                                                                   'RATE', 'GST'))
                    for i in kl:
                        print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format(i[0], i[1], i[2], i[3], i[4],
                                                                                       i[5], i[6]))
            if o == 3:
                tit = input('Enter Item Type\n' + ' => ')
                c.execute(f"select * from items where type='{tit}';")
                kl = c.fetchall()
                if not kl:
                    print('No item found')
                else:
                    print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format('ICODE', 'ITEM NAME', 'COMPANY',
                                                                                   'TYPE',
                                                                                   'STOCK',
                                                                                   'RATE', 'GST'))
                    for i in kl:
                        print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format(i[0], i[1], i[2], i[3], i[4],
                                                                                       i[5], i[6]))
            if o == 4:
                break

    def cd():
        while 1:
            co = int(input(
                ' Available search options:\n' + '  1) By Name\n' + '  2) By Address\n' + '  3) By Phone\n' + '  4) Exit\n' + ' => '))
            if co == 1:
                cn = input('Enter Customer name\n' + ' => ')
                c.execute(f"select * from customers where name='{cn}';")
                kl = c.fetchall()
                if not kl:
                    print('No Customer data found')
                else:
                    print('{0:<15}{1:<10}{2:<15}{3:<15}{4:<7}'.format('CUSTOMERID', 'NAME', 'ADDRESS', 'PHONE',
                                                                      'BALANCE'))
                    for i in kl:
                        print('{0:<15}{1:<10}{2:<15}{3:<15}{4:<7}'.format(i[0], i[1], i[2], i[3], i[4]))
            if co == 2:
                ca = input('Enter Customer Address\n' + ' => ')
                c.execute(f"select * from customers where address='{ca}';")
                kl = c.fetchall()
                if not kl:
                    print('No Customer data found')
                else:
                    print('{0:<12}{1:<10}{2:<15}{3:<15}{4:<7}'.format('CUSTOMERID', 'NAME', 'ADDRESS', 'PHONE',
                                                                      'BALANCE'))
                for i in kl:
                    print('{0:<15}{1:<10}{2:<15}{3:<15}{4:<7}'.format(i[0], i[1], i[2], i[3], i[4]))
            if co == 3:
                cp = input('Enter Customer Phone number\n' + ' => ')
                c.execute(f"select * from customers where name='{cp}';")
                kl = c.fetchall()
                if not kl:
                    print('No Customer data found')
                else:
                    print('{0:<12}{1:<10}{2:<15}{3:<15}{4:<7}'.format('CUSTOMERID', 'NAME', 'ADDRESS', 'PHONE',
                                                                      'BALANCE'))
                    i = kl[0]
                    print('{0:<15}{1:<10}{2:<15}{3:<15}{4:<7}'.format(i[0], i[1], i[2], i[3], i[4]))
            if co == 4:
                break

    def drs():
        while 1:
            i = int(input(
                'Kindly avail yourself of the subsequent choices:\n' + ' 1) Display items with zero stock\n' + ' 2) Display items purchased on a particular day\n' + ' 3) Display total memos generated on a particular day with amount\n' + ' 4) Total payment collection on a particular day\n' + ' 5) List of items sold on a particular day\n' + ' 6) Exit.\n' + ' => '))
            if i == 1:
                c.execute('select * from items where stock = 0;')
                kl = c.fetchall()
                if not kl:
                    print('No item found')
                else:
                    print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format('ICODE', 'ITEM NAME', 'COMPANY',
                                                                                   'TYPE',
                                                                                   'STOCK',
                                                                                   'RATE', 'GST'))
                    for i in kl:
                        print('{0:<10}{1:<20}{2:<20}{3:<15}{4:<10}{5:<8}{6:>3}'.format(i[0], i[1], i[2], i[3], i[4],
                                                                                       i[5], i[6]))
            if i == 2:
                d = input('Enter Date of Purchase (yyyy/mm/dd):' + ' => ')
                c.execute(f"select * from purchase where dop='{d}'")
                kl = c.fetchall()
                if not kl:
                    print('No item purchased on this date.')
                else:
                    print('{0:<10}{1:<13}{2:<10}{3:<15}'.format('ICODE', 'QUANTITY', 'RATE', 'DOP'))
                    for i in kl:
                        print('{0:<10}{1:<13}{2:<10}{3:<15}'.format(i[0], i[1], i[2], i[3]))
            if i == 3:
                d = input('Enter Date of sale (yyyy/mm/dd):' + ' => ')
                c.execute(f"select * from sale where MEMODATE='{d}'")
                kl = c.fetchall()
                if not kl:
                    print('No Memo found')
                else:
                    print('{0:<10}{1:<15}{2:<12}{3:<15}{4:<8}'.format('MEMONO', 'MEMODATE', 'CUSTOMERID', 'TOTALAMOUNT',
                                                                      'TOTALGST'))
                    for i in kl:
                        print('{0:<10}{1:<15}{2:<12}{3:<15}{4:<8}'.format(i[0], i[1], i[2], i[3], i[4]))
            if i == 4:
                e = 0
                d = input('Enter Date of sale (yyyy/mm/dd):' + ' => ')
                c.execute(f"select * from payments where dop='{d}'")
                kl = c.fetchall()
                if not kl:
                    print('No Payment data found')
                else:
                    for i in kl:
                        e = e + i[2]
                        print(f'Total amount collected on {d} : ', e)
            if i == 5:
                d = input('Enter Date of sale (yyyy/mm/dd):' + ' => ')
                c.execute(f"select * from sale where MEMODATE='{d}'")
                kl = c.fetchall()
                if not kl:
                    print('No Memo found')
                else:
                    for i in kl:
                        c.execute(f'select * from itemsold where memono = {i[0]}')
                        ml = c.fetchall()
                        for fd in ml:
                            print('{0:<8}{1:<6}{2:<7}{3:<10}{4:<6}'.format('ICODE', 'QTY', 'RATE', 'AMOUNT', 'GSTAMT'))
                            print('{0:<8}{1:<6}{2:<7}{3:<10}{4:<6}'.format(fd[1], fd[2], fd[3], fd[4], fd[5]))
            else:
                break

    while 1:
        sr = int(input(
            'Select from the following which you want to search for\n' + ' 1) Item(s)\n' + ' 2) Data related to sales\n' + ' 3) Customer data\n' + ' 4) Exit\n' + ' => '))
        if sr == 1:
            si()
        if sr == 2:
            drs()
        if sr == 3:
            cd()
        if sr == 4:
            break


def delt():
    while 1:
        d = int(input(
            'Please select from the following options:\n' + ' 1) Delete sales entry\n' + ' 2) Delete payments entry\n' + ' 3) Delete purchase entry\n' + ' 4) Exit.'))
        if d == 1:
            me = int(input('Enter memo no to remove:\n' + ' => '))
            c.execute(f'select * from sale where memono={me}')
            kl = c.fetchall()
            if not kl:
                print('No Memo found')
            else:
                for i in kl:
                    c.execute(f"update customers set balance=balance - {i[3]}  where customerid='{i[2]}' ")
                    c.execute(f'select * from itemsold where memono={me}')
                    ml = c.fetchall()
                    for sk in ml:
                        c.execute(f"update items set stock= stock + {sk[2]} where icode='{sk[1]}' ")
            c.execute(f'delete from sale where memono={me}')
            yn = input('Save changes ?(Y/N) : ')
            if yn == 'Y' or yn == 'y':
                n.commit()
                n.close()
                print('Database updated :)')
            else:
                n.close()
                print('No changes made :(')
        if d == 2:
            me = int(input('Enter payment memo no to remove payment data:\n' + ' => '))
            c.execute(f'select * from payments where memono={me}')
            kl = c.fetchall()
            if not kl:
                print('No data found')
            else:
                for i in kl:
                    c.execute(f"update customers set balance=balance - {i[2]}  where customerid='{i[0]}' ")
            c.execute(f'delete from payments where memono={me}')
            yn = input('Save changes ?(Y/N) : ')
            if yn == 'Y' or yn == 'y':
                n.commit()
                n.close()
                print('Database updated :)')
            else:
                n.close()
                print('No changes made :(')
        if d == 3:
            d = input('Enter date of purchase (yyyy,mm,dd):\n' + ' => ')
            iid = input('Enter item code:\n' + ' => ')
            c.execute(f"select * from purchase where dop = '{d}' and icode = '{iid}'")
            kl = c.fetchall()
            if not kl:
                print('No Item found')
            else:
                for i in kl:
                    c.execute(f"update items set stock = stock - {i[1]} where icode = '{i[0]}''")
            c.execute(f"delete from purchase where dop={d} and icode='{iid}'")
        else:
            break


while True:
    im = int(input(
        'Welcome To Agency Management System:\n' + 'Available Actions:\n' + '  1) Entry\n' + '  2) Reports\n' + '  3) Delete\n' + '  4) Exit\n' + ' => '))
    if im == 1:
        adr()
    if im == 2:
        srh()
    if im == 3:
        delt()
    if im == 4:
        c.close()
        break
