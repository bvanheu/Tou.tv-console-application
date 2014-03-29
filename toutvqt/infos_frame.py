from pkg_resources import resource_filename
from PyQt4 import uic
from PyQt4 import Qt
from PyQt4 import QtGui
import webbrowser


class QInfosFrame(Qt.QFrame):
    def __init__(self):
        super(QInfosFrame, self).__init__()

        self._setup_ui()
        self.show_infos_none()

    def _swap_infos_widget(self, widget):
        layout = self.layout()

        if layout.count() == 1:
            cur_widget = layout.itemAt(0).widget()
            cur_widget.setParent(None)
        layout.addWidget(widget)

    def show_infos_none(self):
        self._swap_infos_widget(self.none_label)

    def show_emission(self, emission):
        self.emission_widget.set_emission(emission)
        self._swap_infos_widget(self.emission_widget)

    def show_season(self, emission, season_number, episodes):
        self.season_widget.set_infos(emission, season_number, episodes)
        self._swap_infos_widget(self.season_widget)

    def show_episode(self, episode):
        self.episode_widget.set_episode(episode)
        self._swap_infos_widget(self.episode_widget)

    def _setup_none_label(self):
        self.none_label = Qt.QLabel()
        self.none_label.setText('Please select an item in the list above')
        font = Qt.QFont()
        font.setItalic(True)
        self.none_label.setFont(font)

    def _setup_infos_widget(self):
        self.emission_widget = QEmissionInfosWidget()
        self.season_widget = QSeasonInfosWidget()
        self.episode_widget = QEpisodeInfosWidget()

    def _setup_ui(self):
        self.setLayout(Qt.QVBoxLayout())
        self.setFrameShape(Qt.QFrame.Box)
        self.setFrameShadow(Qt.QFrame.Sunken)
        self._setup_none_label()
        self._setup_infos_widget()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding,
                           QtGui.QSizePolicy.Maximum)


class QInfosWidget(Qt.QWidget):
    def __init__(self):
        super(QInfosWidget, self).__init__()

        self._url = None

    def _setup_ui(self, ui_path):
        uic.loadUi(ui_path, baseinstance=self)
        self.goto_toutv_btn.clicked.connect(self._on_goto_toutv_btn_clicked)

    def _set_toutv_url(self, url):
        self._url = url
        if url is None:
            self.goto_toutv_btn.hide()
        else:
            self.goto_toutv_btn.show()

    def _on_goto_toutv_btn_clicked(self):
        if self._url is not None:
            webbrowser.open(self._url)


class QEmissionCommonInfosWidget:
    def _set_common_infos(self, emission):
        country = '-'
        if emission.get_country() is not None:
            country = emission.get_country()
        network = '-'
        if emission.get_network() is not None:
            network = emission.get_network()
        removal_date = '-'
        if emission.get_removal_date() is not None:
            removal_date = str(emission.get_removal_date().date())
        genre = '-'
        if emission.get_genre() is not None:
            genre = emission.get_genre().get_title()

        self.country_value_label.setText(country)
        self.network_value_label.setText(network)
        self.removal_date_value_label.setText(removal_date)
        self.genre_value_label.setText(genre)


class QEmissionInfosWidget(QInfosWidget, QEmissionCommonInfosWidget):
    UI_PATH = resource_filename(__name__, 'dat/ui/emission_infos_widget.ui')

    def __init__(self):
        super(QEmissionInfosWidget, self).__init__()

        self._setup_ui(QEmissionInfosWidget.UI_PATH)

    def set_emission(self, emission):
        title = emission.get_title()
        description = ''
        if emission.get_description() is not None:
            description = emission.get_description()

        self.title_value_label.setText(title)
        self.description_value_label.setText(description)
        self._set_common_infos(emission)

        self._set_toutv_url(emission.get_url())


class QSeasonInfosWidget(QInfosWidget, QEmissionCommonInfosWidget):
    UI_PATH = resource_filename(__name__, 'dat/ui/season_infos_widget.ui')

    def __init__(self):
        super(QSeasonInfosWidget, self).__init__()

        self._setup_ui(QSeasonInfosWidget.UI_PATH)

    def set_infos(self, emission, season_number, episodes):
        nb_episodes = str(len(episodes))

        self.season_number_value_label.setText(str(season_number))
        self.episodes_value_label.setText(nb_episodes)
        self._set_common_infos(emission)

        self._set_toutv_url(emission.get_url())


class QEpisodeInfosWidget(QInfosWidget):
    UI_PATH = resource_filename(__name__, 'dat/ui/episode_infos_widget.ui')

    def __init__(self):
        super(QEpisodeInfosWidget, self).__init__()

        self._setup_ui(QEpisodeInfosWidget.UI_PATH)

    def set_episode(self, episode):
        title = episode.get_title()
        emission_title = episode.get_emission().get_title()
        description = ''
        if episode.get_description() is not None:
            description = episode.get_description()
        sae = '-'
        if episode.get_sae() is not None:
            sae = episode.get_sae()
        air_date = '-'
        if episode.get_air_date() is not None:
            air_date = str(episode.get_air_date())
        length = '-'
        if episode.get_length() is not None:
            minutes, seconds = episode.get_length()
            length = '{}:{:02}'.format(minutes, seconds)

        self.title_value_label.setText(title)
        self.emission_title_value_label.setText(emission_title)
        self.sae_value_label.setText(sae)
        self.air_date_value_label.setText(air_date)
        self.length_value_label.setText(length)
        self.description_value_label.setText(description)

        self._set_toutv_url(episode.get_url())
