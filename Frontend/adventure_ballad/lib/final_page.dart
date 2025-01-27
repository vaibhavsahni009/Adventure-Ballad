import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:background_downloader/background_downloader.dart';
import 'services/request_handler.dart'; // Ensure this import path is correct
import 'dart:convert';

import 'dart:io';
import 'package:path_provider/path_provider.dart';

import 'widgets/app_bar.dart';

class FinalPage extends StatefulWidget {
  final String roomCode;

  FinalPage({required this.roomCode});

  @override
  _FinalPageState createState() => _FinalPageState();
}

class _FinalPageState extends State<FinalPage> {
  final RequestHandler _requestHandler = RequestHandler();
  String _balladSongUrl = '';
  String _balladSongImageUrl = '';
  bool _isLoading = false;
  bool _isPlaying = false;
  AudioPlayer _audioPlayer = AudioPlayer();
  bool _isSongFetched = false;

  Future<void> _fetchBalladSong() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final response = await _requestHandler.getRequest(
        'fetch_final_song/${widget.roomCode}',
      );
      final data = jsonDecode(response.body);

      if (data['song'] != null && data['song'].isNotEmpty) {
        setState(() {
          _balladSongUrl = data['song']['audio_url'].toString();
          _balladSongImageUrl = data['song']['image_url'].toString();
          _isLoading = false;
          _isSongFetched = true;
        });
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      print('An error occurred: $e');
    }
  }

  void _togglePlayPause() async {
    if (_isPlaying) {
      await _audioPlayer.pause();
    } else {
      await _audioPlayer.play(UrlSource(_balladSongUrl));
    }

    setState(() {
      _isPlaying = !_isPlaying;
    });
  }

  Future<void> _downloadSong() async {
    if (_balladSongUrl.isEmpty) return;

    try {
      // Get the appropriate directory for each platform
      Directory directory = Directory('.');

      final task = DownloadTask(
        url: _balladSongUrl,
        filename: 'ballad_song.mp3',
        directory: directory.path,
      );

      await FileDownloader().download(task);

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content:
                Text('Download complete: ${directory.path}/ballad_song.mp3')),
      );
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Download failed: $e')),
      );
    }
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        titleText: 'Final Page',
        // No backgroundColor provided, so it will use the theme's primary color
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Your adventure is complete!',
              style: TextStyle(fontSize: 24),
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 20),
            Text(
              'Download or listen to the ballad song generated about your adventure.',
              textAlign: TextAlign.center,
            ),
            SizedBox(height: 30),
            _isLoading
                ? CircularProgressIndicator()
                : !_isSongFetched
                    ? ElevatedButton(
                        onPressed: _fetchBalladSong,
                        child: Text('Fetch Ballad Song'),
                      )
                    : Column(
                        children: [
                          if (_balladSongImageUrl.isNotEmpty)
                            Image.network(_balladSongImageUrl),
                          SizedBox(height: 10),
                          ElevatedButton(
                            onPressed: _togglePlayPause,
                            child: Text(_isPlaying ? 'Pause' : 'Play'),
                          ),
                          SizedBox(height: 10),
                          ElevatedButton(
                            onPressed: _downloadSong,
                            child: Text('Download Ballad Song'),
                          ),
                          SizedBox(height: 10),
                          Text(
                            'Song URL: $_balladSongUrl',
                            style: TextStyle(fontSize: 16),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
          ],
        ),
      ),
    );
  }
}
