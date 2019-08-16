import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



def load_sample(path_to_gps_file, nrows = 1000000):
    """
    Input: 
        path_to_gps_file is a string that indicates the path to the extracted gps file, e.g., 'data/xian/gps_20161013'
        nrows is the number of rows loaded into the memory, default is 1000000
    Output:
        a dataframe that includes only the first nrows rows of the file, with the 
        column name ['driver_id', 'order_id', 'time', 'lon', 'lat']
    """
    sample = pd.read_csv(path_to_gps_file, 
                 nrows = nrows, 
                 header = None, 
                 names = ['driver_id', 'order_id', 'time', 'lon', 'lat'])
    return sample



def check_vanilla_better_et(sample_vanilla, sample_better):
    """
    Input: 
        sample_vanilla and sample_better are two dataframes containing WGS-84 coordinates
    Output:
        Return True if the two dataframe have the same values inside the box of interest
    """
    n_test = 1000
    _target = sample_vanilla.copy()
    _target2 = sample_better.copy()

    _target = sample_vanilla.loc[(sample_vanilla.lat_wgs > 34.235) & 
                                 (sample_vanilla.lat_wgs < 34.242) & 
                                 (sample_vanilla.lon_wgs > 108.941) & 
                                 (sample_vanilla.lon_wgs < 108.944)].reset_index(drop = True)

    _target2 = sample_better.loc[(sample_better.lat_wgs > 34.236) & 
                                 (sample_better.lat_wgs < 34.243) & 
                                 (sample_better.lon_wgs > 108.940) & 
                                 (sample_better.lon_wgs < 108.945)].reset_index(drop = True)

    _keys = np.random.randint(_target.shape[1], size = n_test)
    _idx = _target[['driver_id', 'order_id', 'time']].values
    for i in range(n_test):
        j = _keys[i]
        assert np.array_equal(_target.loc[j, ['lat_wgs', 'lon_wgs']].values,
                              _target2.loc[(_target2.driver_id == _idx[j, 0])&
                                            (_target2.order_id == _idx[j, 1])&
                                            (_target2.time == _idx[j, 2]), ['lat_wgs', 'lon_wgs']].values[0]), "Test not pass! %d"%i
    print('Evil transform test pass!')
    return True



def check_transform(df_transformed, driver_id, order_id, t_st, t_et):
    """
    Input: 
        df_transformed: A dataframe with WGS-84 coordinates
        driver_id: a string corresponding to a driver_id
        order_id: a string corresponding to an order_id
        t_st, t_et: two integers corresponding to two different times
    Output:
        Returns the latitudes and longitudes of this particular driver in this specific interval of time. Both the latitude and longitude are given with GCJ-2 and WGS-84 coordinates.
    """
    ref_wgs = df_transformed.loc[(df_transformed.driver_id==driver_id)&
                                 (df_transformed.order_id==order_id)&
                                 (df_transformed.time>=t_st)&
                                 (df_transformed.time<=t_et), ['lat', 'lon', 'lat_wgs', 'lon_wgs']].values
    return ref_wgs



def plot_gps(df_transformed):
    """
    Input: 
        df_transformed: A dataframe with WGS-84 coordinates
    Output:
        plot the points contained in the dataframe according to the latitude and longitude
    """
    plt.figure(figsize = (12,8))
    plt.scatter(df_transformed.lon_wgs, df_transformed.lat_wgs, s = 0.5, c = 'k')
    plt.xlim(108.941, 108.944)
    plt.ylim(34.233, 34.242)
    plt.show()
    return