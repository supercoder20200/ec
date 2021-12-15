def atZero(P,Q):
    rVal = (65362673213058167204287320720004833842156409103265307324470271249208562224443, 100)
    Rx, Ry = rVal 
    Px, Py = P
    Qx, Qy = Q
    
    #(Px + Qx > Rx) and  (Py + Qy > Ry)
    if( (Px + Qx) > Rx and (Py + Qy) > Ry ):
        #Qx > Rx > Px  and Qy > Ry > Py
        if( (Qx > Rx and Rx > Px) and (Qy > Ry and Ry > Py) ):
            return False  # No
        else:
            return True   # Yes
    else:
        return False  # No


if __name__ == "__main__":
    Px = 73310771008388540988256401357661415352304042095800324289366824950562794967684
    Py = 9989913769501776956673418849599695616596036032394306022682365229231505097463
    Qx = 48176182141707200397494489313819525051007048199980929464227639919183476022336
    Qy = 6721877582892931413141315114289651970823246064430791708367976298368088092295
    P = (Px, Py)
    Q = (Qx, Qy)
    res = atZero(P, Q)
    print("res: {}".format(res))