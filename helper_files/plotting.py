# this is the helper file for the plotting

import plotly.graph_objects as go

from helper_files.gaussian_fitting import gaussian


def plot_lines(
    x,
    y,
    multiple_y=False,
    list_of_names=None,
    title="Data",
    xaxis_title="x",
    yaxis_title="y",
):
    """
    Using plotly to make a interactive plot of one or multiple sets of data.

    Parameters
    ----------
    x : list
        x values
    y : list
        y values, or list of lists of y values
    multiple_y : bool, optional
        set to True if there are multiple y values, by default False
    list_of_names : list of str, optional
        list of names for the different lines, by default None
    title : str, optional
        figure title, by default 'Data'
    xaxis_title : str, optional
        x axis, by default 'x'
    yaxis_title : str, optional
        y axis, by default 'y'
    """
    # make a figure
    fig = go.Figure()

    if multiple_y:
        # if the length of names is unequal to the length of the lines,
        # or if the lines are not named, make a list of numbers for the names.
        if (list_of_names is None) or len(list_of_names) != len(y):
            list_of_names = [f"line {i}" for i in range(len(y))]

        # loop over the number of lines
        for i in range(len(y)):
            # add a scatter plot to the figure
            fig.add_scatter(x=x, y=y[i], name=list_of_names[i])

    # if there is only one line to plot
    else:
        # add a scatter plot to the figure
        fig.add_scatter(x=x, y=y)
    # set the title, x and y axis titles
    fig.update_layout(title=title, xaxis_title=xaxis_title, yaxis_title=yaxis_title)

    # show the figure
    fig.show()


def fitting_plot(
    x,
    y_raw,
    y_fit=None,
    vlines=None,
    fit_vals=None,
    fig=None,
    start=0,
    stop=2048,
    title="Fitting plot",
    xaxis_title="Channel number [~10eV]",
    yaxis_title="Relative intensity [a.u.]",
):
    """
    Using plotly to make a interactive plot of the data and the fit.
    Can add vertical lines to the plot at the peaks with vlines.
    Can add each gaussian to the plot with fit_vals.

    Parameters
    ----------
    x : list
        the x values
    y_raw : list
        the raw y values
    y_fit : list, optional
        fitted x values, by default None
    vlines : list, optional
        list of x values which should have vertical lines, by default None
    fit_vals : list, optional
        [amp1, mu1, sigma1, amp2, mu2, sigma2, ...], by default None
    fig : plotly.graph_objects.Figure, optional
        if you want to add these plots to an existing figure, by default None
    start : int, optional
        to crop the plot, by default 0
    stop : int, optional
        to crop the plot, by default 2048
    title : str, optional
        figure title, by default "Fitting plot"
    xaxis_title : str, optional
        x axis name, by default "Channel number [~10eV]"
    yaxis_title : str, optional
        y axis name, by default "Relative intensity [a.u.]"

    Returns
    -------
    go.Figure()
        fig, which you eg can save with fig.write_html("filename.html") or fig.show()
    """

    # if no figure is given, make a new one.
    # with this you can plot multiple figures in one plot by calling this function multiple times.
    if fig is None:
        fig = go.Figure()

    # plotting the raw data
    fig.add_trace(
        go.Scatter(
            x=x[start:stop],
            y=y_raw[start:stop],
            mode="lines+markers",
            name=f"raw data",
        )
    )

    # if there is a fit to plot
    if y_fit is not None:  # is false if None
        fig.add_trace(
            go.Scatter(
                x=x[start:stop],
                y=y_fit[start:stop],
                mode="lines",
                name="gaussian fit",
            )
        )

    # add vertical dotted lines with a small annotation, eg for the peak positions
    if vlines is not None:
        for vline in vlines:
            fig.add_vline(
                x=vline,
                line_dash="dot",
                annotation_text=f"{vline:.3f}",
                line_width=0.3,
                annotation_font_size=8,
            )

    # plotting eventual gaussian fitted curves from fit_vals
    if fit_vals is not None:
        for i in range(0, len(fit_vals), 3):
            gauss_y = gaussian(
                x[start:stop], fit_vals[i], fit_vals[i + 1], fit_vals[i + 2]
            )
            fig.add_trace(
                go.Scatter(
                    x=x[start:stop],
                    y=gauss_y,  # is made from [start:stop] above
                    mode="lines",
                    name=f"mu={fit_vals[i]:.2f}, std={fit_vals[i + 1]:.2f}, a={fit_vals[i + 2]:.2f}",
                )
            )

    # set the title, x and y axis titles
    fig.update_layout(
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        legend_title="Legend",
    )

    return fig
