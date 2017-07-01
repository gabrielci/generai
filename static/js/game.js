// Game & Player classes
(function(alseis, $, undefined) {
  // Player class: recieves the player number (no) and the number of sheets (sheets) on instantiation
  // TODO: recieves the name as a parameter

  /* Has the following attributes:
    These two are initialized to the respective input values
      no: Player number (Unique among all players)
      sheets: Number of sheets 
    
    name: Initiated as Null, modified via method "SetName(name)"
    scoresheets: An array containing all scoresheets for the player (It will have a total of scoresheets equal to
                 the "sheets" attribute)
  */
  alseis.Player = function(no, sheets) {
    this.no = no;
    this.sheets = sheets;
    this.name = null;
    this.scoresheets = [];
    var player = this;
    
    // We create "sheets" number of Scoresheets for the current player and we assign the jQuery events that
    // will trigger with its corresponding parameters, Scoresheets are a type of object defined in scoresheet.js
    // both the Scoresheet and Player object use each other on their definition
    for (var i=0; i < sheets; i++) {
      var scoresheet = new alseis.Scoresheet(i, player);

      $(scoresheet).on('score_changed', function(e, scoresheet, play, val, bonus) {
        $(player).trigger('score_changed', [scoresheet, player, play, val, bonus]);
      });
      this.scoresheets.push(scoresheet);
    }
  };

  // We define methods to manipulate the players data, "Note" sets one value on the players Scoresheet,
  // "RemoveNote" removes one value, "SetName" changes the Players name, "GetNNotes" returns the number
  // of marked blocks on a particular sheet or on the entire scoresheet if the input is "null" 
  alseis.Player.prototype.Note = function(sheet, play, val, bonus) {
    this.scoresheets[sheet].Note(play, val, bonus);
  };
  alseis.Player.prototype.RemoveNote = function(sheet, play) {
    this.scoresheets[sheet].RemoveNote(play);
  };
  alseis.Player.prototype.SetName = function(name) {
    this.name = name;
  };
  alseis.Player.prototype.GetNNotes = function(sheet) {
    var n;
    if (sheet == null) {
      for(var i = 0, n = 0; i < this.scoresheets.length; i++)
      {
        n += this.scoresheets[i].nnotes;
      }
    } else {
      n = this.scoresheets[sheet].nnotes;
    }
    return n;
  };

  // We initialize the array that contains the game objects
  alseis.games = [];

// TODO cambiar nombres de estatico a dinamico
// OBSOLETE
  alseis.players = [];

  // Game class: recieves the config object that contains number of players and number of sheets
  // It creates a bunch of attributes and then creates a Player object instance for every player 
  // and links the jQuery events that will update each players sheets
  alseis.Game = function(config)
  {
    this.start_time = Date.now();
    this.end_time = null;
    this.selected_play = null;
    this.config = config;
    this.players = [];
    var game = this;
    for (var i = 0; i < config.nplayers; i++) {
      var player = new alseis.Player(i, config.nsheets);
      $(player).on('score_changed', function(e, scoresheet, player, play, val, bonus) {
        $(game).trigger('score_changed', [scoresheet, player, game, play, val, bonus]);
      });
      this.players.push(player);
    }
  };

  // Gets a particular players number of marked blocks on a particular sheet
  alseis.Game.prototype.GetNNotes = function(player, sheet) {
    return this.players[player].GetNNotes(sheet);
  };

  // Unselects a play made (OBSOLETE?)
  alseis.Game.prototype.UnselectPlay = function(elem) {
    this.selected_play = null;
  };

  // side effect!
  // OBSOLETE? Parece estar conectado a la funcion que abre el menu para seleccionar el score de una casilla
  alseis.Game.prototype.SelectPlay = function(elem)
  {
    var $elem = $(elem);
    var _selectedPlay = {};

    _selectedPlay['player']     = this.players[$elem.data('player')];
    _selectedPlay['scoresheet'] = _selectedPlay['player'].scoresheets[$elem.data('scoresheet')];
    _selectedPlay['play']       = $elem.data('play');

    return this.selected_play = _selectedPlay;
  }

  alseis.Game.prototype.NoteSelected = function(val, bonus) {
    this.selected_play.player.Note(
       this.selected_play.scoresheet.no,
       this.selected_play.play,
       val,
       bonus
    );
    this._selected_play = null;
  };

  alseis.Game.prototype.RemoveNoteSelected = function() {
    this.selected_play.player.RemoveNote(
      this.selected_play.scoresheet.no,
      this.selected_play.play
    );
    this._selected_play = null;
  }

  alseis.Game.prototype.Note = function(player, sheet, play, val, bonus)
  {
    this.players[player].Note(sheet, play, val, bonus);
  };

  alseis.Game.prototype.RemoveNote = function(player, sheet, play) {
    this.players[player].RemoveNote(sheet, play);
  };

  alseis.Game.prototype.PlayersStatus = function() {
    var stats = [];

    for (var i = 0; i < this.config.nsheets; i++) {
        var winning_score = 0;
        var winners = [];
        for (var j = 0; j < this.config.nplayers; j++) {
            var _player = this.players[j];
            var _scoresheet = this.players[j].scoresheets[i];
            var _currentScore = _scoresheet.CurrentScore();
            if (_currentScore > winning_score) {
                winners = [];
                winners.push({player: _player, scoresheet: 1});
                winning_score = _currentScore;
            } else if (_currentScore == winning_score) {
                winners.push(_player);
            }
        }
      
      stats.push({
          'partial_winners_': winners
      });
    }

    return stats;
  };

}( window.alseis = window.alseis || {}, jQuery ));