import os

from click.testing import CliRunner
from rjdl.console import cli

runner = CliRunner()

MUSICS = [
    "https://www.radiojavan.com/mp3s/mp3/Yas-Nameyi-Be-Farzand",
    "https://www.radiojavan.com/mp3s/mp3/EpiCure-Amin-Aminem-Wow-Che-Nice-(Ft-Tensi)",
]

VIDEOS = [
    "https://www.radiojavan.com/videos/video/imanemun-sobhozohroshab-(ft-erfan)",
]

PODCASTS = [
    "https://www.radiojavan.com/podcasts/podcast/Mix-Box-1",
]


def test_cli_version():
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output


def test_music_info():
    result = runner.invoke(
        cli,
        [
            MUSICS[0],
            "-i",
        ],
    )
    assert result.exit_code == 0
    assert "Nameyi Be Farzand" in result.output
    assert "Downloading" not in result.output


def test_video_info():
    result = runner.invoke(
        cli,
        [
            VIDEOS[0],
            "-i",
        ],
    )
    assert result.exit_code == 0
    assert "SobhoZohroShab (Ft Erfan)" in result.output
    assert "Downloading" not in result.output


def test_podcast_info():
    result = runner.invoke(
        cli,
        [
            PODCASTS[0],
            "-i",
        ],
    )
    assert result.exit_code == 0
    assert "Mix Box" in result.output
    assert "Downloading" not in result.output


def test_music():
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                MUSICS[0],
                MUSICS[1],
                "-p",
                "./musics",
            ],
        )
        assert result.exit_code == 0
        assert os.path.exists("./musics/Yas-Nameyi-Be-Farzand.mp3")
        assert os.path.exists(
            "./musics/EpiCure-Amin-Aminem-Wow-Che-Nice-(Ft-Tensi).mp3"
        )


def test_video():
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            [
                VIDEOS[0],
                "-v",
                "480",
            ],
        )
        assert result.exit_code == 0
        assert os.path.exists("./imanemun-sobhozohroshab-(ft-erfan).mp4")
