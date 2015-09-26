import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker

from PIL import Image
from datetime import datetime

from base import BaseScreen
import theoria.graphics as graphics


class UsagePlot(BaseScreen):
    def __init__(self, *args, **kwargs):
        super(UsagePlot, self).__init__(*args, **kwargs)

        self.draw(self._provider.provide())

    def draw(self, data):
        one_gb = 1024 * 1024 * 1024

        # Gather data
        anytime = []
        uploads = []
        freezone = []
        dates = []
        for entry in data['usage']['data']:
            dates.append(datetime.strptime(str(entry['period']), '%Y%m%d'))
            for t in entry['types']:
                if t['type'] == 'anytime':
                    anytime.append(t['value'])
                elif t['type'] == 'uploads':
                    uploads.append(t['value'])
                elif t['type'] == 'freezone':
                    freezone.append(t['value'])


        # Draw the chart
        draw = graphics.TheoriaDraw(self._buf)
        width, height = self._buf.size

        ind = np.arange(len(dates))    # the x locations for the groups
        bar_width = 0.8

        fig, ax = plt.subplots()

        # Set size
        dpi = 70.0
        fig.set_size_inches(width/dpi, height/dpi)
        fig.set_dpi(dpi)

        # Load data
        anytime = np.array(anytime)
        uploads = np.array(uploads)
        freezone = np.array(freezone)

        p1 = plt.bar(dates, anytime,   bar_width, color='r')
        p2 = plt.bar(dates, freezone,  bar_width, color='g', bottom=anytime)
        p3 = plt.bar(dates, uploads,   bar_width, color='b', bottom=anytime+freezone)

        # Legend
        plt.legend((p1[0], p2[0], p3[0]), ('Downloads', 'Freezone', 'Uploads'))

        # Chart Labels
        plt.ylabel('Gigabytes')
        plt.title('Download Usage')

        # X Labels
        somedays = mdates.DayLocator(interval=int(1024/width))
        days     = mdates.DayLocator()
        daysFmt  = mdates.DateFormatter('%-d %b')
        ax.xaxis.set_major_locator(somedays)
        ax.xaxis.set_minor_locator(days)
        ax.xaxis.set_major_formatter(daysFmt)

        # Y Labels
        gb      = ticker.IndexLocator(one_gb, 0)
        fivegb  = ticker.IndexLocator(one_gb * 5, 0)
        gbFmt   = ticker.FuncFormatter(lambda x, p:str(int(x/one_gb)) + ' GB')
        ax.yaxis.set_major_locator(fivegb)
        ax.yaxis.set_minor_locator(gb)
        ax.yaxis.set_major_formatter(gbFmt)

        # Auto format the dates
        fig.autofmt_xdate()
        canvas = plt.get_current_fig_manager().canvas
        canvas.draw()

        # Add Graph
        plot_img = Image.fromstring('RGB', canvas.get_width_height(), canvas.tostring_rgb())
        draw.cpaste(plot_img, (width/2, height/2), center=graphics.CENTER_BOTH)

        self.changed()

