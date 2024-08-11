import 'package:flutter/material.dart';
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
  String _balladSong = '';
  bool _isLoading = false;

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
          _balladSong = data['song'];
          _isLoading = false;
        });
        // Here you can add code to play or download the song
      }
    } catch (e) {
      setState(() {
        _isLoading = false;
      });
      print('An error occurred: $e');
    }
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
                ? CircularProgressIndicator() // Show loading indicator while fetching
                : ElevatedButton(
                    onPressed: _fetchBalladSong,
                    child: Text('Play Ballad Song'),
                  ),
            if (_balladSong.isNotEmpty) // Show song details if available
              Text(
                _balladSong,
                style: TextStyle(fontSize: 16),
                textAlign: TextAlign.center,
              ),
          ],
        ),
      ),
    );
  }
}
