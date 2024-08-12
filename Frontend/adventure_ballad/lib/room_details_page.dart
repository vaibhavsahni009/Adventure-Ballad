import 'dart:async'; // Import this for Timer
import 'dart:convert'; // Import this for jsonDecode
import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'loading_page.dart';
import 'services/request_handler.dart';
import 'widgets/app_bar.dart';

class RoomDetailsPage extends StatefulWidget {
  final String adventurerName;
  final String roomCode;
  final List<String> players;

  RoomDetailsPage({
    required this.adventurerName,
    required this.roomCode,
    required this.players,
  });

  @override
  _RoomDetailsPageState createState() => _RoomDetailsPageState();
}

class _RoomDetailsPageState extends State<RoomDetailsPage> {
  late List<String> players;
  late String adminName;
  late bool isAdmin;
  final RequestHandler requestHandler = RequestHandler();
  late final String roomCode;
  late Timer _pollingTimer;
  bool _isButtonDisabled = false;

  @override
  void initState() {
    super.initState();
    players = widget.players;
    roomCode = widget.roomCode;
    _fetchPlayersList(); // Fetch players list immediately to get the admin info
    _startPolling();
  }

  @override
  void dispose() {
    _pollingTimer
        .cancel(); // Cancel the polling timer when the widget is disposed
    super.dispose();
  }

  Future<void> _fetchPlayersList() async {
    try {
      final response = await requestHandler.getRequest(
        '/api/rooms/$roomCode', // Replace with your actual endpoint path
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        if (mounted) {
          setState(() {
            players = List<String>.from(responseData['players']);
            adminName = responseData['admin'];
            isAdmin = widget.adventurerName == adminName;

            // Navigate to LoadingPage if game_started is true
            if (responseData['game_started'] == true) {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) => LoadingPage(
                    roomCode: widget.roomCode,
                    adventurerName: widget.adventurerName,
                  ),
                ),
              );
            }
          });
        }
      } else {
        throw Exception('Failed to fetch players');
      }
    } catch (e) {
      // Handle exceptions (e.g., network errors)
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('An error occurred: $e'),
          ),
        );
      }
    }
  }

  void _startPolling() {
    const pollingInterval =
        Duration(seconds: 5); // Adjust polling interval as needed
    _pollingTimer = Timer.periodic(pollingInterval, (timer) {
      _fetchPlayersList();
    });
  }

  void _startAdventure(BuildContext context) async {
    if (players.length >= 2) {
      if (isAdmin) {
        if (!_isButtonDisabled) {
          try {
            final response = await requestHandler.postRequest(
              'start_game', // Replace with your actual endpoint path
              {
                'name': widget.adventurerName,
                'code': roomCode,
              },
            );
            print(response);
            print(jsonDecode(response.body));

            if (response.statusCode == 200) {
              // Check if the response is positive, assuming 'success' key indicates success
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (context) => LoadingPage(
                    roomCode: widget.roomCode,
                    adventurerName: widget.adventurerName,
                  ),
                ),
              );
              setState(() {
                _isButtonDisabled = true; // Disable button after clicking
              });
            } else {
              if (mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text('Failed to start the adventure'),
                  ),
                );
              }
            }
          } catch (e) {
            if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(
                  content: Text('An error occurred: $e'),
                ),
              );
              setState(() {
                _isButtonDisabled = false; // Re-enable button if error occurs
              });
            }
          }
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text('Only the admin can start the adventure.'),
            ),
          );
        }
      }
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('You need 2 or more players to start the adventure.'),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(
        titleText: 'Enter Adventurer Name',
        // No backgroundColor provided, so it will use the theme's primary color
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome, ${widget.adventurerName}!',
              style: TextStyle(
                fontSize: 24, // Slightly larger font for the welcome text
                fontWeight: FontWeight.bold,
                color: Colors.deepPurple, // Use a deep purple for elegance
              ),
            ),
            SizedBox(height: 15), // Reduced the gap slightly for better flow
            Text(
              'Room Code: ${widget.roomCode}',
              style: TextStyle(
                fontSize: 18,
                color: Colors.grey[700], // Softer color for the room code
              ),
            ),
            SizedBox(height: 15),
            Text(
              'Players in Room:',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.w600, // Slightly bold for emphasis
                color: Colors.grey[800], // A shade darker for visibility
              ),
            ),
            SizedBox(height: 10),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: players
                  .map((player) => Padding(
                        padding: const EdgeInsets.symmetric(
                            vertical: 5.0), // Add spacing between player names
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.person,
                                color: Colors.deepPurple,
                                size: 20), // Use an icon to represent players
                            SizedBox(width: 8), // Space between icon and text
                            Text(
                              player,
                              style: TextStyle(
                                fontSize: 16,
                                color: Colors
                                    .black87, // Darker color for better readability
                              ),
                            ),
                          ],
                        ),
                      ))
                  .toList(),
            ),
            SizedBox(height: 30),
            fullWidthButton(
              text: 'Leave Room',
              onPressed: () {
                // Implement leave room functionality
              },
            ),
            SizedBox(height: 20),
            Visibility(
              visible: isAdmin,
              child: fullWidthButton(
                text: 'Start Adventure',
                onPressed: () => _startAdventure(context),
                isDisabled: _isButtonDisabled,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
