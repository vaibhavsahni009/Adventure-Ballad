import 'dart:async';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'services/request_handler.dart'; // Make sure this import path is correct
import 'final_page.dart';
import 'widgets/app_bar.dart';

class StoryPage extends StatefulWidget {
  final String roomCode;

  StoryPage({required this.roomCode});

  @override
  _StoryPageState createState() => _StoryPageState();
}

class _StoryPageState extends State<StoryPage> {
  final RequestHandler _requestHandler = RequestHandler();
  String _story = '';
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _pollForStory();
  }

  Future<void> _pollForStory() async {
    Timer.periodic(Duration(seconds: 5), (timer) async {
      try {
        final response = await _requestHandler.getRequest(
          'fetch_final_story/${widget.roomCode}',
        );
        final data = jsonDecode(response.body);
        print(data);
        if (data['final_story'] != null) {
          setState(() {
            _story = data['final_story'];
            _isLoading = false;
          });
          timer.cancel(); // Stop polling once the story is retrieved
        }
      } catch (e) {
        // Handle error if needed
        print('An error occurred: $e');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        titleText: 'Adventure Story',
        // No backgroundColor provided, so it will use the theme's primary color
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: _isLoading
                  ? Center(
                      child:
                          CircularProgressIndicator()) // Show loading indicator while polling
                  : SingleChildScrollView(
                      child: Text(
                        _story,
                        style: TextStyle(fontSize: 18),
                      ),
                    ),
            ),
            SizedBox(height: 20),
            if (!_isLoading) // Show button only if story is retrieved
              fullWidthButton(
                text: 'Listen to adventure Song',
                onPressed: () {
                  _goToSongPage(context);
                },
              ),
          ],
        ),
      ),
    );
  }

  void _goToSongPage(BuildContext context) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => FinalPage(roomCode: widget.roomCode),
      ),
    );
  }
}
