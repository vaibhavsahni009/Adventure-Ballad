import 'package:flutter/material.dart';
import 'package:audioplayers/audioplayers.dart';
import 'services/request_handler.dart'; // Make sure this import path is correct
import 'dart:convert';

class FinalPage extends StatefulWidget {
  final String roomCode;

  FinalPage({required this.roomCode});

  @override
  _FinalPageState createState() => _FinalPageState();
}

class _FinalPageState extends State<FinalPage> {
  final RequestHandler _requestHandler = RequestHandler();
  String _balladSongUrl = '';
  bool _isLoading = false;
  bool _isPlaying = false;
  final AudioPlayer _audioPlayer = AudioPlayer();

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
          _isLoading = false;
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
      print(_isPlaying);
    });
  }

  @override
  void dispose() {
    _audioPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Final Page'),
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
                : ElevatedButton(
                    onPressed: _fetchBalladSong,
                    child: Text('Fetch Ballad Song'),
                  ),
            if (_balladSongUrl.isNotEmpty)
              Column(
                children: [
                  ElevatedButton(
                    onPressed: _togglePlayPause,
                    child: Text(_isPlaying ? 'Pause' : 'Play'),
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
