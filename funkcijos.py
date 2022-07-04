from app import Skaiciuokle
from sqlalchemy import func


def visa_suma():
    try:
        suma = Skaiciuokle.query.with_entities(func.sum(Skaiciuokle.pajamos).label('total')).first().total
        return round(suma)
    except TypeError:
        pass


def saugus_balansas():
    try:
        if visa_suma() < 3500:
            return round(visa_suma() - psd() - vsd())
        else:
            return round(visa_suma() - psd() - vsd() - gpm())
    except TypeError:
        pass


def vsd():
    return visa_suma() // 100 * 12.52


def psd():
    return visa_suma() // 100 * 6.98


def gpm():
    return visa_suma() // 100 * 5


def atideta_mokesciams():
    try:
        return round(visa_suma() - saugus_balansas())
    except TypeError:
        pass

