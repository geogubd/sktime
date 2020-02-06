import numpy as np
from sktime.utils.validation.forecasting import check_consistent_time_index, validate_time_index, validate_y

__author__ = ['Markus Löning']
__all__ = ["mase_loss", "smape_loss"]

# for reference implementations, see https://github.com/M4Competition/M4-methods/blob/master/ML_benchmarks.py


def mase_loss(y_test, y_pred, y_train, sp=1):
    """Mean absolute scaled error.

    This scale-free error metric can be used to compare forecast methods on a single
    series and also to compare forecast accuracy between series. This metric is well
    suited to intermittent-demand series because it never gives infinite or undefined
    values.

    Parameters
    ----------
    y_test : pandas Series of shape = (fh,) where fh is the forecasting horizon
        Ground truth (correct) target values.
    y_pred : pandas Series of shape = (fh,)
        Estimated target values.
    y_train : pandas Series of shape = (n_obs,)
        Observed training values.
    sp : int
        Seasonal periodicity of training data.

    Returns
    -------
    loss : float
        MASE loss

    References
    ----------
    ..[1]   Hyndman, R. J. (2006). "Another look at measures of forecast accuracy", Foresight, Issue 4.
    """

    # input checks
    y_test = validate_y(y_test)
    y_pred = validate_y(y_pred)
    y_train = validate_y(y_train)
    check_consistent_time_index(y_test, y_pred, y_train=y_train)

    #  naive seasonal prediction
    y_train = np.asarray(y_train)
    y_pred_naive = y_train[:-sp]

    # mean absolute error of naive seasonal prediction
    mae_naive = np.mean(np.abs(y_train[sp:] - y_pred_naive))

    return np.mean(np.abs(y_test - y_pred)) / mae_naive


def smape_loss(y_test, y_pred):
    """Symmetric mean absolute percentage error

    Parameters
    ----------
    y_test : pandas Series of shape = (fh,) where fh is the forecasting horizon
        Ground truth (correct) target values.
    y_pred : pandas Series of shape = (fh,)
        Estimated target values.

    Returns
    -------
    loss : float
        SMAPE loss
    """
    check_consistent_time_index(y_test, y_pred)

    nominator = np.abs(y_test - y_pred)
    denominator = np.abs(y_test) + np.abs(y_pred)
    return np.mean(2.0 * nominator / denominator)