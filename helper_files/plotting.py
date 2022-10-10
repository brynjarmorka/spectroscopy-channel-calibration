# this is the helper file for the plotting

import plotly.graph_objects as go

from helper_files.gaussian_fitting import area_under_peak, gaussian


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
    fig.show(renderer="notebook")


def plotly_plot(
    x=None,
    y=None,
    y_fit=None,
    y_named=None,
    vlines=None,
    vlines_name=None,
    fit_params=None,
    fig=None,
    start=0,
    stop=2048,
    title="Untitled",
    xaxis_title="Channel number [~10eV]",
    yaxis_title="Relative intensity",
):
    """
    Using plotly to make a interactive plot of the data and the fit.
    Can add vertical lines to the plot at the peaks with vlines.
    Can add each gaussian to the plot with fit_params.

    Parameters
    ----------
    x : list, optional
        the x values
    y : list, optional
        y values
    y_fit : list, optional
        fitted x values, by default None
    y_named : list, optional
        [y_values_list, name_as_string] a named line to be plotted
    vlines : list, optional
        list of x values which should have vertical lines, by default None
    vlines_name : list, optional
        list of names for the vertical lines, by default None
    fit_params : list, optional
        [amp1, mu1, std1, amp2, mu2, std2, ...], by default None
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
        y axis name, by default "Relative intensity"

    Returns
    -------
    go.Figure()
        fig, which you eg can save with fig.write_html("filename.html") or fig.show()
    """

    if x is None:
        print("You must specify the x values! Returned None")
        return None

    # if no figure is given, make a new one.
    # with this you can plot multiple figures in one plot by calling this function multiple times.
    if fig is None:
        fig = go.Figure()

    # plotting the raw data
    if y is not None:
        fig.add_trace(
            go.Scatter(
                x=x[start:stop],
                y=y[start:stop],
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

    if y_named is not None:
        fig.add_trace(
            go.Scatter(
                x=x[start:stop],
                y=y_named[0][start:stop],
                mode="lines",
                name=y_named[1],
            )
        )

    # # add vertical dotted lines with a small annotation, eg for the peak positions
    # if vlines is not None:
    #     for vline in vlines:
    #         fig.add_vline(
    #             x=vline,
    #             line_dash="dot",
    #             annotation_text=f"{vline:.3f}",
    #             line_width=0.3,
    #             annotation_font_size=8,
    #         )

    # add vertical dotted lines with a small annotation, eg for the peak positions
    if vlines is not None:
        for i in range(len(vlines)):
            vline = vlines[i]

            # adding names to the lines
            try:
                line_name = f"{vlines_name[i]}: {vline:.4f}"
            except (IndexError, TypeError):
                line_name = f"{vline:.4f}"
            fig.add_trace(
                go.Scatter(
                    x=[vline, vline],
                    y=[-0.05, 1],
                    line_dash="dot",
                    line_width=1,
                    text=[line_name, line_name],
                    textposition="bottom right",
                    mode="lines+text",
                    name=line_name,
                    marker=dict(color="black"),
                )
            )
            fig.update_traces(textfont_size=8)

    # plotting eventual gaussian fitted curves from fit_vals
    if fit_params is not None:
        for i in range(0, len(fit_params), 3):
            gauss_y = gaussian(
                x[start:stop], fit_params[i], fit_params[i + 1], fit_params[i + 2]
            )
            area = area_under_peak(fit_params[i + 1], fit_params[2 + i], fit_params[i])
            fig.add_trace(
                go.Scatter(
                    x=x[start:stop],
                    y=gauss_y,  # is made from [start:stop] above
                    mode="lines",
                    name=f"a={fit_params[i]:.2f}, mu={fit_params[i + 1]:.2f}, std={fit_params[i + 2]:.2f}, area={area:.3f}",
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
