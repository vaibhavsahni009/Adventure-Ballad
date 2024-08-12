import 'package:flutter/material.dart';
import 'common_widgets.dart';
import 'greeting_page.dart';
import 'widgets/app_bar.dart';

class EnterNamePage extends StatefulWidget {
  @override
  _EnterNamePageState createState() => _EnterNamePageState();
}

class _EnterNamePageState extends State<EnterNamePage> {
  final TextEditingController _nameController = TextEditingController();

  void _submitName() {
    final enteredName = _nameController.text;
    if (enteredName.isNotEmpty) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => GreetingPage(adventurerName: enteredName),
        ),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Please enter your name'),
        ),
      );
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
            customTextField(
                controller: _nameController, label: 'Enter your name'),
            SizedBox(height: 20),
            fullWidthButton(
              text: 'Submit',
              onPressed: _submitName,
            ),
          ],
        ),
      ),
    );
  }
}
