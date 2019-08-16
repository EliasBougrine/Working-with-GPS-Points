# -*- coding: utf-8 -*-
# Source code from: https://github.com/googollee/eviltransform/blob/master/python/eviltransform/__init__.py
import math
import numpy as np



# __all__ = ['wgs2gcj', 'gcj2wgs', 'gcj2wgs_exact',
#            'distance', 'gcj2bd', 'bd2gcj', 'wgs2bd', 'bd2wgs']

earthR = 6378137.0



# Return True if the lat and long are out of China
def outOfChina(lat, lng):
    return not (72.004 <= lng <= 137.8347 and 0.8293 <= lat <= 55.8271)



#Transform x and y in a lat and a long
def transform(x, y):
	xy = x * y
	absX = math.sqrt(abs(x))
	xPi = x * math.pi
	yPi = y * math.pi
	d = 20.0*math.sin(6.0*xPi) + 20.0*math.sin(2.0*xPi)

	lat = d
	lng = d

	lat += 20.0*math.sin(yPi) + 40.0*math.sin(yPi/3.0)
	lng += 20.0*math.sin(xPi) + 40.0*math.sin(xPi/3.0)

	lat += 160.0*math.sin(yPi/12.0) + 320*math.sin(yPi/30.0)
	lng += 150.0*math.sin(xPi/12.0) + 300.0*math.sin(xPi/30.0)

	lat *= 2.0 / 3.0
	lng *= 2.0 / 3.0

	lat += -100.0 + 2.0*x + 3.0*y + 0.2*y*y + 0.1*xy + 0.2*absX
	lng += 300.0 + x + 2.0*y + 0.1*x*x + 0.1*xy + 0.1*absX

	return lat, lng



# Compute the difference between GCJ2 and WGS84 coordinates
def delta(lat, lng):
    ee = 0.00669342162296594323
    dLat, dLng = transform(lng-105.0, lat-35.0)
    radLat = lat / 180.0 * math.pi
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((earthR * (1 - ee)) / (magic * sqrtMagic) * math.pi)
    dLng = (dLng * 180.0) / (earthR / sqrtMagic * math.cos(radLat) * math.pi)
    return dLat, dLng



# Transform WGS84 coordinates into GCJ2 coordinates
def wgs2gcj(wgsLat, wgsLng):
    if outOfChina(wgsLat, wgsLng):
        return wgsLat, wgsLng
    else:
        dlat, dlng = delta(wgsLat, wgsLng)
        return wgsLat + dlat, wgsLng + dlng



# Transform GCJ2 coordinates into WGS84 coordinates
def gcj2wgs(gcjLat, gcjLng):
    if outOfChina(gcjLat, gcjLng):
        return gcjLat, gcjLng
    else:
        dlat, dlng = delta(gcjLat, gcjLng)
        return gcjLat - dlat, gcjLng - dlng



# Transform GCJ2 coordinates into WGS84 coordinates with more accuracy
def gcj2wgs_exact(gcjLat, gcjLng):
    initDelta = 0.01
    
    threshold = 0.000001
    dLat = dLng = initDelta
    mLat = gcjLat - dLat
    mLng = gcjLng - dLng
    pLat = gcjLat + dLat
    pLng = gcjLng + dLng
    for i in range(30):
        wgsLat = (mLat + pLat) / 2
        wgsLng = (mLng + pLng) / 2
        tmplat, tmplng = wgs2gcj(wgsLat, wgsLng)
        dLat = tmplat - gcjLat
        dLng = tmplng - gcjLng
        if abs(dLat) < threshold and abs(dLng) < threshold:
            return wgsLat, wgsLng
        if dLat > 0:
            pLat = wgsLat
        else:
            mLat = wgsLat
        if dLng > 0:
            pLng = wgsLng
        else:
            mLng = wgsLng
    return wgsLat, wgsLng



# Distance
def distance(latA, lngA, latB, lngB):
    pi180 = math.pi / 180
    arcLatA = latA * pi180
    arcLatB = latB * pi180
    x = (math.cos(arcLatA) * math.cos(arcLatB) *
         math.cos((lngA - lngB) * pi180))
    y = math.sin(arcLatA) * math.sin(arcLatB)
    s = x + y
    if s > 1:
        s = 1
    if s < -1:
        s = -1
    alpha = math.acos(s)
    distance = alpha * earthR
    return distance
    


# Define the vectorized functions

transform_vectorized = np.vectorize(transform)

delta_vectorized = np.vectorize(delta)

def wgs2gcj_vectorized(wgsLat, wgsLng):
    wgsLat = np.array(wgsLat)
    wgsLng = np.array(wgsLng)
    dlat, dlng = delta_vectorized(wgsLat, wgsLng)
    return wgsLat + dlat, wgsLng + dlng
    
def gcj2wgs_vectorized(gcjLat, gcjLng):
    gcjLat = np.array(gcjLat)
    gcjLng = np.array(gcjLng)
    dlat, dlng = delta_vectorized(gcjLat, gcjLng)
    return gcjLat - dlat, gcjLng - dlng
    
gcj2wgs_exact_vectorized = np.vectorize(gcj2wgs_exact)


